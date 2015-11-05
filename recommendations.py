# region Data
from math import sqrt

critics = {
    'Lisa Rose': {
        'Lady in the Water': 2.5,
        'Shakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'Superman Returns': 3.5,
        'You, Me and Dupree': 2.5,
        'The Night Listener': 3.0
    },
    'Gene Seymour': {
        'Lady in the Water': 3.0,
        'Shakes on a Plane': 3.5,
        'Just My Luck': 1.5,
        'Superman Returns': 5.0,
        'You, Me and Dupree': 3.0,
        'The Night Listener': 3.5
    },
    'Michael Phillips': {
        'Lady in the Water': 2.5,
        'Shakes on a Plane': 3.0,
        'Superman Returns': 3.5,
        'The Night Listener': 4.0
    },
    'Claudia Puig': {
        'Shakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'Superman Returns': 4.0,
        'You, Me and Dupree': 2.5,
        'The Night Listener': 4.5
    },
    'Mick LaSalle': {
        'Lady in the Water': 3.0,
        'Shakes on a Plane': 4.0,
        'Just My Luck': 2.0,
        'Superman Returns': 3.0,
        'You, Me and Dupree': 2.0,
        'The Night Listener': 3.0
    },
    'Jack Matthews': {
        'Lady in the Water': 3.0,
        'Shakes on a Plane': 4.0,
        'Superman Returns': 5.0,
        'You, Me and Dupree': 4.0,
        'The Night Listener': 3.0
    },
    'Toby': {
        'Shakes on a Plane': 4.5,
        'Superman Returns': 4.0,
        'You, Me and Dupree': 1.0,
    }
}


# endregion


def sim_distance(prefs, person1, person2):
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1
    if len(si) == 0:
        return 0
    sum_of_squares = sum([
                             pow(prefs[person1][item] - prefs[person2][item], 2) for item in prefs[person1] if
                             item in prefs[person2]
                             ])

    return 1 / (1 + sum_of_squares)


def sim_pearson(prefs, p1, p2):
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1
    n = len(si)
    if n == 0:
        return 0

    sum1 = sum([prefs[p1][item] for item in si])
    sum2 = sum([prefs[p2][item] for item in si])

    sum1Sq = sum([pow(prefs[p1][item], 2) for item in si])
    sum2Sq = sum([pow(prefs[p2][item], 2) for item in si])

    pSum = sum([prefs[p2][item] * prefs[p1][item] for item in si])

    num = pSum - (sum1 * sum2) / n
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))

    if den == 0:
        return 0

    return num / den


def top_matches(prefs, person, n=5, similarity=sim_pearson):
    scores = [
        (similarity(prefs, person, other), other) for other in prefs if other != person
        ]

    scores.sort()
    scores.reverse()

    return scores[0:n]


def get_recommendations(prefs, person, similarity=sim_pearson):
    totals = {}
    simSums = {}

    for other in prefs:
        if other == person:
            continue
        sim = similarity(prefs, person, other)
        if sim <= 0:
            continue
        for item in prefs[other]:
            if item not in prefs[person] or prefs[person][item] == 0:
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim
                simSums.setdefault(item, 0)
                simSums[item] += sim
    rankings = [(total / simSums[item], item) for item, total in totals.items()]
    rankings.sort()
    rankings.reverse()
    return rankings

def load_movie_lens(path='ml-100k/'):
    movies = {}
    for line in open(path + '/u.item'):
        (movie_id, title) = line.split('|')[0:2]
        movies[movie_id] = title
    prefs = {}
    for line in open(path + '/u.data'):
        (user, movie_id, rating, ts) = line.split('\t')
        prefs.setdefault(user, {})
        prefs[user][movies[movie_id]] = float(rating)
    return prefs

def transform_prefs(prefs):
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})
            result[item][person] = prefs[person][item]
    return result

def calculate_similar_items(prefs, n=10):
    result = {}
    item_prefs = transform_prefs(prefs)
    for item in item_prefs:
        scores = top_matches(item_prefs, item, n=n, similarity=sim_distance)
        result[item] = scores
    return result

def get_recommended_items(prefs, item_match, user):
    user_ratings = prefs[user]
    scores = {}
    total_sim = {}
    for (item, rating) in user_ratings.items():
        for (similarity, item2) in item_match[item]:
            if item2 in user_ratings:
                continue
            scores.setdefault(item2, 0)
            scores[item2] += similarity * rating
            total_sim.setdefault(item2, 0)
            total_sim[item2] += similarity
    rankings = [(score / total_sim[item], item) for item, score in scores.items()]
    rankings.sort()
    rankings.reverse()
    return rankings


prefs = load_movie_lens()
print get_recommendations(prefs, '87')[0:30]
item_sim = calculate_similar_items(prefs, n=50)
print get_recommended_items(prefs, item_sim, '87')[0:30]

