"""
Calculate page rank
"""


"""
graph is a dictionary of nodes
"""
def compute_rank(graph):
    """
    damping factor: probability that user clicks a link on the current page
    """
    d = 0.8

    # number of times we'll go through the relaxation
    # higher > higher accuracy of rank
    numloop = 10

    ranks = {}
    npages = len(graph)

    # initialize ranks evenly
    for page in graph:
        ranks[page] = 1.0 / npages

    for i in range(numloop):
        # update newranks using formula based on ranks
        # then assign newranks to ranks
        newranks = {}
        for page in graph:
            """
            compute the new rank for current page
            that reflects the probability of starting from this page
            and the popularity based on inbound links
            """
            newrank = (1-d) / npages

            """
            update by summing in the inlink ranks:
            + sum (d * rank(p, t - 1) / number of outlinks from p)
            over all pages p that link to this page
            """
            for p in graph:
                p_links = graph[p]
                if page in p_links:
                    newrank += (d * ranks[p] / len(p_links))

            newranks[page] = newrank
        ranks = newranks
    return ranks


graph = {'http://one.com/': [], 'http://one.com/hello': ['http://unicorns.com', 'https://turtles.com'], 'http://unicorns.com': ['http://one.com/'], 'https://turtles.com': ['http://unicorns.com'], 'https://hummus.com/forever/': [], 'http://udacity.com/cs101x/urank/index.html': ['https://hummus.com/forever/', 'https://turtles.com', 'http://one.com/', 'http://unicorns.com', 'http://one.com/hello']}

print(compute_rank(graph))