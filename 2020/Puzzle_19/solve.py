def parse_rule(line, rules):
    irule, rule = line.split(": ")
    irule = int(irule)
    if '"' in rule:
        val = rule[1]
    else:
        val = tuple(
            [tuple([int(e) for e in f.split(" ") if e != ""]) for f in rule.split("|")]
        )
    rules[irule] = val


def check_rule(entry, rules, i, irule=0):
    rule = rules[irule]

    if isinstance(rule, str):
        return (entry[0] == rule,)
    else:
        for i, ruleset in enumerate(rules):
            pass


lines = open("input_test2").read().split("\n")

rules = {}
for line in lines:
    if line == "":
        break
    parse_rule(line, rules)

entries = "babbbbaabbbbbabbbbbbaabaaabaaa"

for entry in entries:
    check_rule(entry, rules)
