import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from anonymization.utils.normalizer import StringNormalizer
from anonymization.utils.hasher import DeterministicHasher
from anonymization.utils.name_generator import NameGenerator

test_data = [
    "John",
    "MARY",
    "  Alice  ",
    "Bob",
    "john",
    "José",
    "alice@example.com",
    None,
    ""
]

print("=" * 80)
print("Testing Name Anonymization Flow")
print("=" * 80)

normalizer = StringNormalizer()
hasher = DeterministicHasher()
name_gen = NameGenerator(locale='en_US')

print(f"\nGenerated salt: {hasher.get_salt().hex()[:32]}...\n")

for original in test_data:
    print(f"Original: {original!r}")
    
    normalized = normalizer.normalize(original)
    print(f"  → Normalized: {normalized!r}")
    
    if normalized:
        hash_int = hasher.hash_to_int(normalized)
        print(f"  → Hash Int: {hash_int}")
        
        first_name = name_gen.get_first_name(hash_int)
        print(f"  → First Name: {first_name}")
        
        last_name = name_gen.get_last_name(hash_int)
        print(f"  → Last Name: {last_name}")
    else:
        print(f"  → Skipped (empty)")
    
    print()

print("=" * 80)
print("Testing Collision Handling (same normalized value)")
print("=" * 80)

name_gen2 = NameGenerator(locale='en_US')
test_collisions = ["John", "JOHN", "john", "  John  "]

results = []
for name in test_collisions:
    normalized = normalizer.normalize(name)
    hash_int = hasher.hash_to_int(normalized)
    pseudo = name_gen2.get_first_name(hash_int)
    results.append((name, normalized, pseudo))
    print(f"{name!r:20} → normalized: {normalized!r:10} → {pseudo}")

print("\n✓ All should map to the SAME pseudonym (deterministic)")
all_same = len(set([r[2] for r in results])) == 1
print(f"✓ Test passed: {all_same}")

print("\n" + "=" * 80)
print("Testing Different Names Get Unique Pseudonyms")
print("=" * 80)

name_gen3 = NameGenerator(locale='en_US')
different_names = ["Alice", "Bob", "Charlie", "Diana", "Eve"]

pseudonyms = []
for name in different_names:
    normalized = normalizer.normalize(name)
    hash_int = hasher.hash_to_int(normalized)
    pseudo = name_gen3.get_first_name(hash_int)
    pseudonyms.append(pseudo)
    print(f"{name:15} → {pseudo}")

print(f"\nUnique pseudonyms: {len(set(pseudonyms))} / {len(pseudonyms)}")
all_unique = len(set(pseudonyms)) == len(pseudonyms)
print(f"✓ All unique test passed: {all_unique}")

