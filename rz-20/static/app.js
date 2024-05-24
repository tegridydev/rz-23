async function fetchBitcoinData() {
    const response = await fetch('/bitcoin');
    const data = await response.json();
    return data;
}

async function fetchData() {
    const response = await fetch('/blocks');
    const blocks = await response.json();

    const totalBlocks = blocks.length;
    const totalRizz = blocks.reduce((sum, block) => sum + block.reward, 0);
    const totalStorage = blocks.reduce((sum, block) => sum + block.compressed_data, 0);
    const totalHashrate = blocks.length;

    document.getElementById('total-blocks-mined').textContent = `Total Blocks Mined: ${totalBlocks}`;
    document.getElementById('total-rizz-supply').textContent = `Total RIZZ Supply: ${totalRizz.toFixed(2)}`;
    document.getElementById('total-storage-size').textContent = `Total Storage Size: ${(totalStorage / 1024).toFixed(2)} KB`;
    document.getElementById('total-hashrate').textContent = `Total Hashrate: ${totalHashrate} H/s`;

    const bitcoinData = await fetchBitcoinData();
    document.getElementById('bitcoin-block-height').textContent = `Bitcoin Block Height: ${bitcoinData.height}`;
    document.getElementById('bitcoin-hashrate').textContent = `Bitcoin Hashrate: ${bitcoinData.difficulty}`;
    document.getElementById('bitcoin-block-number').textContent = `Bitcoin Block Number: ${bitcoinData.id}`;

    const ctx = document.getElementById('blockChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: blocks.map(block => `Block ${block.id}`),
            datasets: [{
                label: 'RIZZ Reward',
                data: blocks.map(block => block.reward),
                borderColor: 'rgba(75,192,192,1)',
                backgroundColor: 'rgba(75,192,192,0.2)',
                fill: true,
            }],
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Trigger new RIZZ block on new Bitcoin block
    if (bitcoinData.height !== localStorage.getItem('lastBitcoinBlockHeight')) {
        localStorage.setItem('lastBitcoinBlockHeight', bitcoinData.height);
        await fetch('/trigger', { method: 'POST' });
        fetchData();
    }
}

window.onload = fetchData;
