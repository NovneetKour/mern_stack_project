document.addEventListener('DOMContentLoaded', () => {
    const monthSelect = document.getElementById('month-select');
    const searchBox = document.getElementById('search-box');
    const transactionsTableBody = document.querySelector('#transactions-table tbody');
    const prevPageButton = document.getElementById('prev-page');
    const nextPageButton = document.getElementById('next-page');
    const totalSaleAmount = document.getElementById('total-sale-amount');
    const totalSoldItems = document.getElementById('total-sold-items');
    const totalNotSoldItems = document.getElementById('total-not-sold-items');
    const barChartCanvas = document.getElementById('bar-chart');
    let currentPage = 1;
    let currentMonth = '03';

    const fetchData = async (url) => {
        const response = await fetch(url);
        return response.json();
    };

    const updateTable = async () => {
        const search = searchBox.value;
        const url = `/transactions?month=${currentMonth}&search=${search}&page=${currentPage}`;
        const data = await fetchData(url);

        transactionsTableBody.innerHTML = '';
        data.forEach(transaction => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${transaction.id}</td>
                <td>${transaction.title}</td>
                <td>${transaction.description}</td>
                <td>${transaction.price}</td>
                <td>${transaction.date_of_sale}</td>
                <td>${transaction.category}</td>
                <td>${transaction.sold}</td>
            `;
            transactionsTableBody.appendChild(row);
        });
    };

    const updateStatistics = async () => {
        const url = `/statistics?month=${currentMonth}`;
        const data = await fetchData(url);

        totalSaleAmount.innerText = `Total Sale Amount: ${data.total_sales_amount}`;
        totalSoldItems.innerText = `Total Sold Items: ${data.total_sold_items}`;
        totalNotSoldItems.innerText = `Total Not Sold Items: ${data.total_not_sold_items}`;
    };

    const updateBarChart = async () => {
        const url = `/bar-chart?month=${currentMonth}`;
        const data = await fetchData(url);

        const labels = Object.keys(data);
        const values = Object.values(data);

        const ctx = barChartCanvas.getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Number of items',
                    data: values,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    };

    const updatePage = async () => {
        await updateTable();
        await updateStatistics();
        await updateBarChart();
    };

    monthSelect.addEventListener('change', async (e) => {
        currentMonth = e.target.value;
        currentPage = 1;
        await updatePage();
    });

    searchBox.addEventListener('input', async () => {
        currentPage = 1;
        await updateTable();
    });

    prevPageButton.addEventListener('click', async () => {
        if (currentPage > 1) {
            currentPage--;
            await updateTable();
        }
    });

    nextPageButton.addEventListener('click', async () => {
        currentPage++;
        await updateTable();
    });

    // Initial load
    updatePage();
});
