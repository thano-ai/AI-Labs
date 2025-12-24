function initVisualizer(filename) {
    const evtSource = new EventSource(`/stream/${filename}`);
    const frontierEl = document.getElementById('frontier');
    const visitedEl = document.getElementById('visited');
    const logEl = document.getElementById('log');
    const svg = d3.select('#graph-svg');
    let buffer = [];
    let playing = false;

    evtSource.onmessage = (e) => {
        try {
            const obj = JSON.parse(e.data);
            buffer.push(obj);
            if (!playing) renderState(obj);
        } catch(err) {
            console.error('parse', err, e.data);
        }
    };

    document.getElementById('btn-play').onclick = () => { playing = true; playLoop(); };
    document.getElementById('btn-pause').onclick = () => { playing = false; };
    document.getElementById('btn-step').onclick = () => { if(buffer.length) renderState(buffer.shift()); };

    function playLoop() {
        if(!playing) return;
        if(buffer.length) renderState(buffer.shift());
        setTimeout(playLoop, 300);
    }

    function renderState(msg) {
        if(msg.error){
            logEl.textContent = 'ERROR:\n'+ (msg.traceback||JSON.stringify(msg));
            return;
        }

        const st = msg.state || msg;
        frontierEl.textContent = JSON.stringify(st.frontier || st.queue || st.stack || st.heap || []);
        visitedEl.textContent = JSON.stringify(st.visited || []);
        let logText = '';
        if(st.current) logText += 'current: '+st.current+'\n';
        if(st.node) logText += 'node: '+st.node+'\n';
        if(st.goal_found) logText += 'Goal found!\n';
        logEl.textContent = logText;

        // Simple graph visualization
        svg.selectAll('*').remove();
        const w = +svg.attr('width'), h = +svg.attr('height');
        const nodes = st.visited || [];
        nodes.forEach((n,i)=>{
            svg.append('circle')
                .attr('cx', 50 + i*50)
                .attr('cy', h/2)
                .attr('r', 20)
                .attr('fill', '#3B82F6');
            svg.append('text')
                .attr('x', 50 + i*50)
                .attr('y', h/2 + 6)
                .attr('text-anchor','middle')
                .attr('font-size',12)
                .text(n);
        });
        if(st.current){
            svg.append('circle')
                .attr('cx', w-50)
                .attr('cy', h/2)
                .attr('r', 25)
                .attr('fill','#FBBF24');
            svg.append('text')
                .attr('x', w-50)
                .attr('y', h/2 + 6)
                .attr('text-anchor','middle')
                .attr('font-size',16)
                .text(st.current);
        }
    }
}
