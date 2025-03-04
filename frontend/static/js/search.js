document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');
    const filterButton = document.getElementById('filter-button');
    const filterDropdown = document.querySelector('.filter-dropdown');
    const storeTypeFilter = document.getElementById('store-type-filter');
    const promotionsFilter = document.getElementById('promotions-filter');
    const resultsContainer = document.getElementById('results-container');
    const homeSearchInput = document.getElementById('home-search-input');
    const homeSearchButton = document.getElementById('home-search-button');

    const updateFilters = () => {
        const filters = [];
        if (storeTypeFilter && storeTypeFilter.checked) { filters.push("Store Type"); }
        if (promotionsFilter && promotionsFilter.checked) { filters.push("Promotions"); }
        
        // Get current URL search parameters
        const urlParams = new URLSearchParams(window.location.search);
        // Preserve the search query
        const searchQuery = urlParams.get('search') || '';
        urlParams.delete('filter');
        // Append each active filter
        filters.forEach(filter => urlParams.append('filter', filter));
        
        // Reload page with updated parameters so backend filters the results
        window.location.search = urlParams.toString();
    };

    searchButton.addEventListener('click', () => {
        const query = searchInput.value;
        const selectedFilters = [];
        if (storeTypeFilter.checked) selectedFilters.push("Store Type");
        if (promotionsFilter.checked) selectedFilters.push("Promotions");

        const apiUrl = `/api/search?q=${encodeURIComponent(query)}&filter=${selectedFilters.join('&filter=')}`;

        fetch(apiUrl)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`); // Throw error for non-200 responses
                }
                return response.json();
            })
            .then(data => {
                displayResults(data);
            })
            .catch(error => {
                console.error("Error fetching data:", error);
                resultsContainer.innerHTML = "<p>Error fetching data. Please try again later.</p>";
            });
    });

    homeSearchButton.addEventListener('click', () => {
        const query = homeSearchInput.value;
        const encodedQuery = encodeURIComponent(query);
        window.location.href = `{{ url_for('web.search_results') }}?search=${encodedQuery}`;
    });

    filterButton.addEventListener('click', () => {
        filterDropdown.style.display = (filterDropdown.style.display === 'block') ? 'none' : 'block';
    });

    if (storeTypeFilter) {
        storeTypeFilter.addEventListener('change', updateFilters);
    }
    if (promotionsFilter) {
        promotionsFilter.addEventListener('change', updateFilters);
    }

    // URL parameter handling (for searches from home.html)
    const urlParams = new URLSearchParams(window.location.search);
    const initialSearch = urlParams.get('search');
    if (initialSearch) {
        searchInput.value = decodeURIComponent(initialSearch);
        searchButton.click();
    } else {
        // Fetch all data for the initial display (if needed)
        fetch('/api/search')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => displayResults(data))
            .catch(error => console.error("Error fetching initial data:", error));
    }

    // Show the filter dropdown if on the search results page
    if (window.location.pathname.includes('search-results')) {
        filterDropdown.style.display = 'block'; // Show the dropdown by default
    }

    // Function to render search results in tile format
    const renderSearchResults = (results) => {
        resultsContainer.innerHTML = ''; // Clear previous results

        results.forEach(result => {
            const tile = document.createElement('div');
            tile.className = 'tile';
            tile.innerHTML = `
                <h2>${result.title}</h2>
                <p>${result.description}</p>
            `;
            resultsContainer.appendChild(tile);
        });
    };

    // Example: Simulate fetching results (replace this with actual fetch logic)
    const exampleResults = [
        { title: 'Store 1', description: 'Description for Store 1' },
        { title: 'Store 2', description: 'Description for Store 2' },
        { title: 'Promotion 1', description: 'Latest deals on shoes.' },
        { title: 'Event 1', description: 'Upcoming event at The Centrepoint.' }
    ];

    // Call renderSearchResults with example data (remove this in production)
    renderSearchResults(exampleResults);
});