

chrome.action.onClicked.addListener(tab => {
    chrome.scripting.executeScript({
        target: {tabId: tab.id},
        func: () => {
            function makeElementDraggable(el) {
                let offsetX = 0, offsetY = 0, isDragging = false;
            
                el.style.position = 'fixed'; // allow absolute movement
                el.style.cursor = 'move';    // show move cursor
                el.style.top = '40px';
                el.style.right = '20px';
            
                document.addEventListener('mousedown', (e) => {
                    if ((el.getBoundingClientRect().left+500 >= e.clientX && e.clientX >= el.getBoundingClientRect().left) && (el.getBoundingClientRect().top >= e.clientY && e.clientY >= el.getBoundingClientRect().top-35)){
                        console.log("True")
                        isDragging = true;
                        offsetX = e.clientX - el.getBoundingClientRect().left;
                        offsetY = e.clientY - el.getBoundingClientRect().top;
                        e.preventDefault();
                    }
                });
            
                document.addEventListener('mousemove', (e) => {
                    console.log("Mouse moved")
                    if (!isDragging) return;
                    console.log("Drag registeres", e.clientX - offsetX, e.clientY - offsetY)
                    el.style.left = `${e.clientX - offsetX}px`;
                    el.style.top = `${e.clientY - offsetY}px`;
                });
            
                document.addEventListener('mouseup', (e) => {
                    isDragging = false;
                    console.log("Mouse up")
                });
            }

            if (!document.getElementById('my-extension-iframe')) {
                const iframe = document.createElement('iframe');
                iframe.id = 'my-extension-iframe';
                iframe.src = chrome.runtime.getURL('index.html');
                iframe.style = `
                  position: fixed;
                  width: 600px;
                  height: 600px;
                  border: none;
                  z-index: 2147483647;
                  background: transparent;
                `;
                document.body.appendChild(iframe);
                makeElementDraggable(iframe);
            }
            
            
        }
    })
});


