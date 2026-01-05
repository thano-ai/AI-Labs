class TSPVisualizer {
    constructor() {
        this.canvas = document.getElementById('tspCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.cities = [];
        this.bestPath = [];
        this.currentGen = 0;
        this.bestDistance = Infinity;
        this.animationId = null;
        this.isRunning = false;
        this.population = [];

        this.init();
        this.loadCities();
        this.setupEventListeners();
        this.drawCities();
    }

    async init() {
        // Initialize parameters from sliders
        this.updateSliderValues();

        // Load initial city list
        await this.loadCities();
        this.drawCities();
    }

    async loadCities() {
        try {
            const response = await fetch('/api/cities');
            this.cities = await response.json();
            this.updateCityList();
        } catch (error) {
            console.error('Error loading cities:', error);
        }
    }

    updateCityList() {
        const cityList = document.getElementById('cityList');
        cityList.innerHTML = '';

        this.cities.forEach((city, index) => {
            const cityItem = document.createElement('div');
            cityItem.className = 'city-item';
            cityItem.innerHTML = `
                <span class="city-index">#${index + 1}</span>
                <strong>${city.name}</strong>
                <div class="city-coords">${city.lat.toFixed(2)}, ${city.lng.toFixed(2)}</div>
            `;
            cityList.appendChild(cityItem);
        });
    }

    setupEventListeners() {
        // Run button
        document.getElementById('runBtn').addEventListener('click', () => this.runAlgorithm());

        // Reset button
        document.getElementById('resetBtn').addEventListener('click', () => this.reset());

        // Step button
        document.getElementById('stepBtn').addEventListener('click', () => this.stepGeneration());

        // Update slider values
        const sliders = ['populationSize', 'generations', 'mutationRate', 'elitism'];
        sliders.forEach(sliderId => {
            const slider = document.getElementById(sliderId);
            const valueSpan = document.getElementById(sliderId + 'Value');

            slider.addEventListener('input', () => {
                valueSpan.textContent = parseFloat(slider.value).toFixed(2);
            });
        });
    }

    updateSliderValues() {
        document.getElementById('populationValue').textContent =
            document.getElementById('populationSize').value;
        document.getElementById('generationsValue').textContent =
            document.getElementById('generations').value;
        document.getElementById('mutationValue').textContent =
            parseFloat(document.getElementById('mutationRate').value).toFixed(2);
        document.getElementById('elitismValue').textContent =
            document.getElementById('elitism').value;
    }

    async runAlgorithm() {
        if (this.isRunning) return;

        this.isRunning = true;
        this.currentGen = 0;
        this.bestDistance = Infinity;

        document.getElementById('runBtn').innerHTML = '<i class="fas fa-pause"></i> Pause';
        document.getElementById('runBtn').onclick = () => this.pauseAlgorithm();

        const params = this.getAlgorithmParams();

        try {
            const response = await fetch('/api/solve', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(params)
            });

            const result = await response.json();
            this.showFinalResult(result);

            // Animate the path
            this.animatePath(result.path_indices);

        } catch (error) {
            console.error('Error running algorithm:', error);
        } finally {
            this.isRunning = false;
            document.getElementById('runBtn').innerHTML = '<i class="fas fa-play"></i> Run Algorithm';
            document.getElementById('runBtn').onclick = () => this.runAlgorithm();
        }
    }

    pauseAlgorithm() {
        this.isRunning = false;
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
        document.getElementById('runBtn').innerHTML = '<i class="fas fa-play"></i> Run Algorithm';
        document.getElementById('runBtn').onclick = () => this.runAlgorithm();
    }

    async stepGeneration() {
        // Simulate one generation step
        this.currentGen++;
        this.updateGenerationDisplay();

        // Update statistics
        this.updateStats();

        // Redraw with current best path
        this.drawCities();
        if (this.bestPath.length > 0) {
            this.drawPath(this.bestPath, '#4361ee', 3);
        }
    }

    getAlgorithmParams() {
        return {
            population_size: parseInt(document.getElementById('populationSize').value),
            generations: parseInt(document.getElementById('generations').value),
            mutation_rate: parseFloat(document.getElementById('mutationRate').value),
            elitism: parseInt(document.getElementById('elitism').value),
            selection_method: document.getElementById('selectionMethod').value,
            start_city: document.getElementById('startCity').value || null,
            end_city: document.getElementById('endCity').value || null
        };
    }

    showFinalResult(result) {
        document.getElementById('finalDistance').textContent = result.distance.toFixed(2);
        document.getElementById('foundAtGen').textContent = result.generation_found;
        document.getElementById('bestPath').textContent = result.path.join(' → ');
    }

    drawCities() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        if (this.cities.length === 0) return;

        // Calculate bounds
        const lats = this.cities.map(c => c.lat);
        const lngs = this.cities.map(c => c.lng);
        const minLat = Math.min(...lats);
        const maxLat = Math.max(...lats);
        const minLng = Math.min(...lngs);
        const maxLng = Math.max(...lngs);

        // Scale cities to canvas
        const padding = 60;
        const scaleX = (this.canvas.width - padding * 2) / (maxLng - minLng);
        const scaleY = (this.canvas.height - padding * 2) / (maxLat - minLat);
        const scale = Math.min(scaleX, scaleY);

        // Draw city points
        this.cities.forEach((city, index) => {
            const x = padding + (city.lng - minLng) * scale;
            const y = this.canvas.height - padding - (city.lat - minLat) * scale;

            // Draw city circle
            this.ctx.beginPath();
            this.ctx.arc(x, y, 8, 0, Math.PI * 2);
            this.ctx.fillStyle = '#4361ee';
            this.ctx.fill();
            this.ctx.strokeStyle = 'white';
            this.ctx.lineWidth = 2;
            this.ctx.stroke();

            // Draw city label
            this.ctx.fillStyle = '#333';
            this.ctx.font = 'bold 14px Inter';
            this.ctx.textAlign = 'center';
            this.ctx.fillText(city.name.substring(0, 3), x, y - 15);
            this.ctx.font = '10px Inter';
            this.ctx.fillText(`#${index + 1}`, x, y + 25);
        });
    }

    drawPath(pathIndices, color = '#4361ee', width = 3) {
        if (pathIndices.length < 2) return;

        const padding = 60;
        const lats = this.cities.map(c => c.lat);
        const lngs = this.cities.map(c => c.lng);
        const minLat = Math.min(...lats);
        const maxLat = Math.max(...lats);
        const minLng = Math.min(...lngs);
        const maxLng = Math.max(...lngs);
        const scaleX = (this.canvas.width - padding * 2) / (maxLng - minLng);
        const scaleY = (this.canvas.height - padding * 2) / (maxLat - minLat);
        const scale = Math.min(scaleX, scaleY);

        this.ctx.beginPath();

        pathIndices.forEach((cityIndex, i) => {
            const city = this.cities[cityIndex];
            const x = padding + (city.lng - minLng) * scale;
            const y = this.canvas.height - padding - (city.lat - minLat) * scale;

            if (i === 0) {
                this.ctx.moveTo(x, y);
            } else {
                this.ctx.lineTo(x, y);
            }
        });

        // Close the loop
        const firstCity = this.cities[pathIndices[0]];
        const firstX = padding + (firstCity.lng - minLng) * scale;
        const firstY = this.canvas.height - padding - (firstCity.lat - minLat) * scale;
        this.ctx.lineTo(firstX, firstY);

        this.ctx.strokeStyle = color;
        this.ctx.lineWidth = width;
        this.ctx.lineCap = 'round';
        this.ctx.lineJoin = 'round';
        this.ctx.stroke();
    }

    animatePath(pathIndices) {
        let currentSegment = 0;
        const segmentDuration = 50; // ms per segment
        const totalSegments = pathIndices.length;

        const animate = () => {
            if (currentSegment <= totalSegments) {
                this.drawCities();

                // Draw completed path segments
                if (currentSegment > 1) {
                    const completedPath = pathIndices.slice(0, currentSegment);
                    this.drawPath(completedPath, '#4361ee', 3);
                }

                // Draw current moving point
                if (currentSegment < totalSegments) {
                    const startIdx = pathIndices[currentSegment];
                    const startCity = this.cities[startIdx];

                    const padding = 60;
                    const lats = this.cities.map(c => c.lat);
                    const lngs = this.cities.map(c => c.lng);
                    const minLat = Math.min(...lats);
                    const maxLat = Math.max(...lats);
                    const minLng = Math.min(...lngs);
                    const maxLng = Math.max(...lngs);
                    const scaleX = (this.canvas.width - padding * 2) / (maxLng - minLng);
                    const scaleY = (this.canvas.height - padding * 2) / (maxLat - minLat);
                    const scale = Math.min(scaleX, scaleY);

                    const x = padding + (startCity.lng - minLng) * scale;
                    const y = this.canvas.height - padding - (startCity.lat - minLat) * scale;

                    // Draw moving point
                    this.ctx.beginPath();
                    this.ctx.arc(x, y, 12, 0, Math.PI * 2);
                    this.ctx.fillStyle = '#f72585';
                    this.ctx.fill();
                    this.ctx.strokeStyle = 'white';
                    this.ctx.lineWidth = 3;
                    this.ctx.stroke();
                }

                currentSegment++;
                this.animationId = setTimeout(animate, segmentDuration);
            } else {
                // Animation complete, draw final path
                this.drawCities();
                this.drawPath(pathIndices, '#4361ee', 3);
            }
        };

        animate();
    }

    updateGenerationDisplay() {
        document.getElementById('currentGen').textContent = this.currentGen;
        document.getElementById('bestDistance').textContent = this.bestDistance.toFixed(2);
    }

    updateStats() {
        // Simulate some statistics for demo
        const avgFitness = 1000 / (this.currentGen + 1);
        const bestFitness = 500 / (this.currentGen + 1);
        const improvement = ((1000 - bestFitness) / 1000 * 100).toFixed(1);

        document.getElementById('avgFitness').textContent = avgFitness.toFixed(2);
        document.getElementById('bestFitness').textContent = bestFitness.toFixed(2);
        document.getElementById('improvement').textContent = `${improvement}%`;
    }

    reset() {
        this.isRunning = false;
        this.currentGen = 0;
        this.bestDistance = Infinity;
        this.bestPath = [];

        if (this.animationId) {
            clearTimeout(this.animationId);
        }

        this.updateGenerationDisplay();
        this.drawCities();

        // Reset UI
        document.getElementById('finalDistance').textContent = '-';
        document.getElementById('foundAtGen').textContent = '-';
        document.getElementById('bestPath').textContent = '-';

        this.updateStats();
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.tspVisualizer = new TSPVisualizer();
});