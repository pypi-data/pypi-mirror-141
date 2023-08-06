from logboss.tracer import LogBoss
from logboss import rules
from dataclasses import dataclass
from pathlib import Path
import os


logger = LogBoss(rule_set=rules.RuleSet(rules=[
    (rules.Class(include=['TestIt']), rules.Function(include=['__init__', '(?!_).*'])),#, exclude=['_.*'])),
    (rules.Function(include=['_private']))
]))
logger.start()

print()

@dataclass
class TestIt:
    a: str
    b: int

    def add(self, x: int):
        items = os.listdir(os.path.expanduser('~'))
        return self.b + x

    @staticmethod
    def logit(msg: str = None):
        msg = msg or 'meh'
        logger.info(msg)

    def _private(self):
        print('Not logged!!!')


def main():
    testit = TestIt(
        a='Here is a simple message.',
        b=1
    )
    testit.add(1)
    testit.logit()
    testit.logit('Here is an overriden simple message.')
    testit._private()


if __name__ == '__main__':
    main()

"""
logger = LogBoss(
    rules=LogRuleSet([
        (
            LogRule.Module(include=['pytpp'], exclude['pytpp._.*']),
            LogRule.BaseClass(include=['FeatureBase', 'APIBase']),
        ),
    ], [
        (
            LogRule.Class(exclude=['_.*'])
            LogRule.Function(exclude=['_.*'])
        ),        
    ]
)
"""
