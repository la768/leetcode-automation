import json

b = {}
b.update(json.load(open('friend_bank200.json', encoding='utf-8')))
b.update(json.load(open('friend_bank100.json', encoding='utf-8')))

slugs = ['add-to-array-form-of-integer', 'button-with-longest-push-time',
         'calculate-digit-sum-of-a-string',
         'check-if-strings-can-be-made-equal-with-operations-i',
         'consecutive-characters', 'arrange-coins', 'construct-rectangle']
for s in slugs:
    print('#' * 25, s)
    print(b.get(s))
