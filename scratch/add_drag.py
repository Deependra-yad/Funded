import re

with open('app/templates/admin_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

drag_script = '''
<script>
// Make window-mode tabs draggable
document.addEventListener('DOMContentLoaded', () => {
    let isDragging = false;
    let currentX;
    let currentY;
    let initialX;
    let initialY;
    let xOffset = 0;
    let yOffset = 0;
    let activeWindow = null;

    document.querySelectorAll('.window-header').forEach(header => {
        header.addEventListener('mousedown', dragStart);
    });

    document.addEventListener('mouseup', dragEnd);
    document.addEventListener('mousemove', drag);

    function dragStart(e) {
        if (e.target.closest('button')) return; // ignore window controls
        activeWindow = e.target.closest('.window-mode');
        if (!activeWindow) return;
        
        // Bring to front
        document.querySelectorAll('.window-mode').forEach(w => w.style.zIndex = '100');
        activeWindow.style.zIndex = '101';

        const style = window.getComputedStyle(activeWindow);
        const matrix = new WebKitCSSMatrix(style.transform);
        xOffset = matrix.m41;
        yOffset = matrix.m42;

        initialX = e.clientX - xOffset;
        initialY = e.clientY - yOffset;
        isDragging = true;
    }

    function dragEnd(e) {
        initialX = currentX;
        initialY = currentY;
        isDragging = false;
        activeWindow = null;
    }

    function drag(e) {
        if (isDragging && activeWindow) {
            e.preventDefault();
            currentX = e.clientX - initialX;
            currentY = e.clientY - initialY;
            activeWindow.style.transform = `translate(${currentX}px, ${currentY}px)`;
        }
    }
});
</script>
'''

if 'function dragStart' not in content:
    content = content.replace('</body>', drag_script + '\n</body>')
    with open('app/templates/admin_dashboard.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("DRAG SCRIPT ADDED")
