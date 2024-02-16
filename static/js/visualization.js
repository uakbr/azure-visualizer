// Visualization.js for Azure Permissions Visualizer

document.addEventListener('DOMContentLoaded', function() {
    // Check if the permissions map container exists
    const permissionsMapContainer = document.getElementById('permissions-map');
    if (permissionsMapContainer) {
        // Initialize the visualization
        initPermissionsMap();
    }
});

function initPermissionsMap() {
    // Placeholder for actual data fetching and visualization logic
    // This example uses D3.js for visualization

    // Normally, you would fetch the permissions data from your backend here
    // For demonstration, let's use a static dataset
    const permissionsData = [
        { id: "1", type: "Role", name: "Administrator", children: [
            { id: "2", type: "User", name: "John Doe" },
            { id: "3", type: "User", name: "Jane Doe" }
        ]},
        { id: "4", type: "Role", name: "Reader", children: [
            { id: "5", type: "User", name: "Jim Beam" }
        ]}
    ];

    // Setup the base SVG element
    const svg = d3.select('#permissions-map').append('svg')
        .attr('width', 800)
        .attr('height', 600)
        .style('background-color', '#fff')
        .style('border', '1px solid #ccc');

    // Setup the root hierarchy for D3
    const root = d3.hierarchy({children: permissionsData})
        .sum(d => 1) // Define how to calculate the node value
        .sort((a, b) => b.value - a.value);

    // Create a d3 tree layout
    const treeLayout = d3.tree().size([800, 500]);
    treeLayout(root);

    // Add links (connections between nodes)
    svg.selectAll('.link')
        .data(root.links())
        .enter().append('path')
        .attr('class', 'link')
        .attr('d', d3.linkHorizontal()
            .x(d => d.y)
            .y(d => d.x))
        .style('fill', 'none')
        .style('stroke', '#888')
        .style('stroke-width', '2px');

    // Add nodes
    const node = svg.selectAll('.node')
        .data(root.descendants())
        .enter().append('g')
        .attr('class', 'node')
        .attr('transform', d => `translate(${d.y},${d.x})`);

    // Add circles for each node
    node.append('circle')
        .attr('r', 10)
        .style('fill', '#69b3a2')
        .style('stroke', '#000')
        .style('stroke-width', '2px');

    // Add labels for each node
    node.append('text')
        .attr('dy', '.35em')
        .attr('x', d => d.children ? -15 : 15)
        .style('text-anchor', d => d.children ? 'end' : 'start')
        .text(d => d.data.name || d.data.type)
        .style('font-size', '12px');
}

