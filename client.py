import nftables
import json

class Nftables:
    def __init__(self, port, comment):
        self.nft = nftables.Nftables()
        self.nft.set_json_output(True)
        self.port = port
        self.comment = comment

    def get_rules(self):
        rules_list = []
        rc, output, error = self.nft.cmd('list chain filter INPUT')
        json_output = json.loads(output)['nftables']
        count = 0
        while count < len(json_output):
            try:
                rules_list.append(json_output[count]['rule'])
                count += 1
            except KeyError:
                count += 1

        return rules_list

    def delete_rule(self):
        current_rules = self.get_rules()
        rule_to_delete = dict(nftables=[])
        rule_to_delete['nftables'] = []
        for rule in current_rules:
            if rule.get('comment') == self.comment and rule.get('expr')[0]['match']['right'] == self.port:
                rule_to_delete['nftables'].append(rule)
                pass

        delete_rule_command = dict(nftables=[])
        delete_rule_command['nftables'] = []
        delete_rule_command['nftables'].append(dict(metainfo=dict(json_schema_version=1)))
        delete_rule_command['nftables'].append(dict(delete=dict(rule=rule_to_delete)))

        print(delete_rule_command)

        self.nft.json_validate(rule_to_delete)

        rc, output, error = self.nft.cmd(json.dumps(delete_rule_command))
        print(rc)
        print(output)
        print(error)
