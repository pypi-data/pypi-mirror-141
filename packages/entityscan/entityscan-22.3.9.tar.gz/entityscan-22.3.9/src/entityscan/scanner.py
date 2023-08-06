from pathlib import Path
from logging import INFO
from typing import Iterable, List
from itertools import chain
import json

from pony import orm

from entityscan import (
    Connection,
    Pipeline,
    Rule,
    Doc,
    Entity,
    engines,
    timelog,
    logger,
)


class Scanner:

    _scanner = None

    def __init__(
        self,
        db_url: str = None,
        connection: Connection = None,
        encoding: str = None,
    ):
        assert db_url or connection, "Missing both db url or connection."
        self.db_url = db_url
        self.connection = connection or Connection(db_url=db_url)
        self.encoding = encoding or "UTF-8"
        self.patterns = engines.PatternEngine(encoding=self.encoding)
        self.composites = engines.CompositeEngine()
        self.literals = engines.LiteralEngine()

    @classmethod
    def instance(cls, db_url: str, encoding: str = None):
        if not cls._scanner:
            cls._scanner = cls(db_url=db_url, encoding=encoding)
            cls._scanner.compile()
        else:
            assert db_url == cls._scanner.db_url, "Incongruent DB URL"
        return cls._scanner

    @orm.db_session
    def load_rules(self, rules_jsonl: Path):
        assert rules_jsonl.suffix == ".jsonl", "Only supports JSONL files."
        for line in rules_jsonl.open("r"):
            line = line.strip()
            if line and line.startswith("{"):
                try:
                    kw = json.loads(line)
                    kw["has_groups"] = "(?P<" in kw.get("pattern", "")
                    Rule(**kw)
                except json.JSONDecodeError:
                    logger.exception(f"JSON Fail: {line[:30]}...{line[-30:]}")
                    raise

    @orm.db_session
    @timelog("compile", level=INFO)
    def compile(self):
        for rule in Rule.select():
            if rule.is_pattern:
                self.patterns.add_rule(rule)
            elif rule.is_composite:
                self.composites.add_rule(rule)
            elif rule.is_literal:
                self.literals.add_rule(rule)
            else:
                raise ValueError(f"Invalid rule: {rule.id}")

        self.patterns.compile()
        self.literals.compile()

        return self

    @orm.db_session
    def scan_expressions(self, text: str) -> List[Entity]:
        p_entities = self.patterns.scan(text)
        l_entities = self.literals.scan(text)
        return Entity.sort_filter(chain(p_entities, l_entities))

    def scan(self, text: str, pipeline: str = None) -> List[Entity]:
        entities = self.scan_expressions(text=text)
        entities = self.composites.process(text, entities)
        entities = Entity.sort_filter(entities)

        if pipeline:
            entities = Pipeline.run(pipeline, text, entities)
            entities = Entity.sort_filter(entities)
        return entities

    def parse(self, text: str, pipeline: str = None) -> Doc:
        return Doc(text=text, entities=self.scan(text))

    def find(self, text: str, labels: Iterable[str] = None) -> List[Entity]:
        entities = self.scan(text)
        if labels:
            labels = set(labels)
            entities = [ent for ent in entities if ent.label in labels]
        return entities

    def find_one(self, text: str, labels: Iterable[str] = None):
        entities = self.find(text=text, labels=labels)
        return entities[0] if len(entities) == 1 else None
