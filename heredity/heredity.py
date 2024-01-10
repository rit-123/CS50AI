import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    # if len(sys.argv) != 2:
    #     sys.exit("Usage: python heredity.py data.csv")
    # people = load_data(sys.argv[1])
    people = load_data("data/family0.csv")

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    no_gene = set()
    no_trait = set()
    for person in people:
        if (person not in one_gene) and (person not in two_genes):
            no_gene.add(person)
        if person not in have_trait:
            no_trait.add(person)

    conditional_probabilities = dict()

    # dictionary to store all the calculated probabilites 
    for person in people:
        conditional_probabilities[person] = {"gene": 0.0, "trait": 0.0}

    for person in people:
        
        # GENE PROBABILITIES

        # if no parents, use unconditional probabilities of having the gene
        if (people[person]["mother"] == None) and (people[person]["father"] == None):
            if person in one_gene:
                conditional_probabilities[person]["gene"] = PROBS["gene"][1]
            if person in two_genes:
                conditional_probabilities[person]["gene"] =  PROBS["gene"][2]
            if person in no_gene:
                conditional_probabilities[person]["gene"] = PROBS["gene"][0]
        else:
            mother = prob_of_passing(one_gene, two_genes, no_gene, people[person]["mother"])
            father = prob_of_passing(one_gene, two_genes, no_gene, people[person]["father"])
            # checking for 2gene
            if person in two_genes:
                conditional_probabilities[person]["gene"] = mother * father
            # checking for 1gene
            if person in one_gene:
                conditional_probabilities[person]["gene"] = (mother * (1 - father)) + (father * (1 - mother))
            # checking for 0gene
            if person in no_gene:
                conditional_probabilities[person]["gene"] = (1 - mother) * (1 - father)

        # TRAIT PROBABILITIES
        
        # checking for 0gene   
        if person in no_gene:
            if person in no_trait:
                conditional_probabilities[person]["trait"] = PROBS["trait"][0][False]
            else:
                conditional_probabilities[person]["trait"] = PROBS["trait"][0][True]
        if person in one_gene:
            if person in no_trait:
                conditional_probabilities[person]["trait"] = PROBS["trait"][1][False]
            else:
                conditional_probabilities[person]["trait"] = PROBS["trait"][1][True]
        if person in two_genes:
            if person in no_trait:
                conditional_probabilities[person]["trait"] = PROBS["trait"][2][False]
            else:
                conditional_probabilities[person]["trait"] = PROBS["trait"][2][True]

    joint_prob = 1
    for person in conditional_probabilities:
        joint_prob = joint_prob * conditional_probabilities[person]["gene"] * conditional_probabilities[person]["trait"]
    print("JOINT PROB:" ,joint_prob)
    return joint_prob

def prob_of_passing(one_gene, two_genes, no_gene, parent_to_check):
    if parent_to_check in one_gene:
        return 0.5
    if parent_to_check in two_genes:
        return 1 * (1 - PROBS["mutation"]) + 0 * (PROBS["mutation"])
    if parent_to_check in no_gene:
        return 0 * (1 - PROBS["mutation"]) + 1 * (PROBS["mutation"])


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    no_gene = set()
    no_trait = set()
    for person in probabilities:
        if (person not in one_gene) and (person not in two_genes):
            no_gene.add(person)
        if person not in have_trait:
            no_trait.add(person)

    for person in probabilities:
        if person in no_gene:
            probabilities[person]["gene"][0] += p
        if person in one_gene:
            probabilities[person]["gene"][1] += p
        if person in two_genes:
            probabilities[person]["gene"][2] += p
        if person in have_trait:
            probabilities[person]["trait"][True] += p
        if person in no_trait:
            probabilities[person]["trait"][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        
        # gene distribution
        sum = probabilities[person]["gene"][0] + probabilities[person]["gene"][1] + probabilities[person]["gene"][2]
        probabilities[person]["gene"][0] = probabilities[person]["gene"][0]/sum
        probabilities[person]["gene"][1] = probabilities[person]["gene"][1]/sum
        probabilities[person]["gene"][2] = probabilities[person]["gene"][2]/sum

        # trait
        sum = probabilities[person]["trait"][True] + probabilities[person]["trait"][False]
        probabilities[person]["trait"][True] = probabilities[person]["trait"][True]/sum
        probabilities[person]["trait"][False] = probabilities[person]["trait"][False]/sum


if __name__ == "__main__":
    main()
