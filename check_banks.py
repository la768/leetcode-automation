import json

t = json.load(open('friend_bank_topup.json', encoding='utf-8'))
print('topup size:', len(t))
print('has sum-of-squares-of-special-elements:', 'sum-of-squares-of-special-elements' in t)
print('last 5 keys:', list(t)[-5:])
f = json.load(open('friend_bank_fix.json', encoding='utf-8'))
print('fix bank:', list(f))
