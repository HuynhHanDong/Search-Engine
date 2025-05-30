import numpy as np

def pagerank_iterative(transition_matrix, damping_factor=0.85, max_iter=100, tolerance=1.0e-6):
    """ Calculate PageRank using iterative method """
    # Number of pages
    n = transition_matrix.shape[0]

    # Start with equal PageRank for all pages 
    pagerank = np.ones(n) / n

    # Teleportation Constant
    teleport = (1 - damping_factor) / n

    for i in range(max_iter):
        # Damping factor: the chance that a user will follow a link from the current page
        # Teleport: equal probability a user jumping to any random page
        new_pagerank = damping_factor * transition_matrix @ pagerank + teleport

        # Stop if the change between iterations is very small
        if np.linalg.norm(new_pagerank - pagerank, 1) < tolerance:
            break

        pagerank = new_pagerank

    return pagerank

def pagerank_matrix(transition_matrix, damping_factor=0.85):
    """ Calculate PageRank using matrix method """
    # Number of pages
    n = transition_matrix.shape[0]

    # Create n×n identity matrix
    I = np.eye(n)

    # Teleportation Constant
    teleport = (1 - damping_factor) / n
 
    # (I - damping_factor * transition_matrix) * pagerank = teleportation_vector
    A = I - damping_factor * transition_matrix
    
    # teleportation_vector
    b = np.ones(n) * teleport
    
    # Solve the linear equation
    pagerank = np.linalg.solve(A, b)
    
    return pagerank

def display_results(pagerank_iter, pagerank_matrix):
    """ Display PageRank results from highest to lowest """
    pages = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6']
    print("PageRank results (highest to lowest):")
    print("-"*60)

    print("Iterative method:")
    iter_ranking = sorted(enumerate(pages), key=lambda x: pagerank_iter[x[0]], reverse=True)
    for rank, (idx, page) in enumerate(iter_ranking, 1):
        print(f"  {rank}. {page}: {pagerank_iter[idx]:.6f}")
    
    print("\nMatrix method:")
    matrix_ranking = sorted(enumerate(pages), key=lambda x: pagerank_matrix[x[0]], reverse=True)
    for rank, (idx, page) in enumerate(matrix_ranking, 1):
        print(f"  {rank}. {page}: {pagerank_matrix[idx]:.6f}")


def main():
    """
    Graph Structure:
    P1 -> P2, P3
    P2 
    P3 -> P1, P2, P4
    P4 -> P6
    P5 -> P4, P6
    P6 -> P4
    """
    # Transition matrix: columns represent outbound links
    transition_matrix = np.array([
        [0,   0,   1/3, 0,   0,   0],
        [1/2, 0,   1/3, 0,   0,   0],
        [1/2, 0,   0,   0,   0,   0],
        [0,   0,   1/3, 0,   1/2, 1],
        [0,   0,   0,   0,   0,   0],
        [0,   0,   0,   1,   1/2, 0]
    ])

    # Iterative method result
    pagerank_iter = pagerank_iterative(transition_matrix)
    print("Iterative method:", pagerank_iter)

    # Matrix method result
    pagerank_matrix_result = pagerank_matrix(transition_matrix)
    print("Matrix method:", pagerank_matrix_result)

    # Display pageRank results in nice format
    print("="*60)
    display_results(pagerank_iter, pagerank_matrix_result)

if __name__ == "__main__":
    main()
