/* Enhancement only: native links, details, and the TOC work without JavaScript. */
(()=>{const root=document.documentElement;let size=parseFloat(getComputedStyle(root).fontSize);const status=document.getElementById('reader-size-status');status.textContent=size+'px';
for(const button of document.querySelectorAll('[data-reader-size]'))button.addEventListener('click',()=>{size=Math.max(16,Math.min(24,size+Number(button.dataset.readerSize)));root.style.setProperty('--reader-size',size+'px');root.style.fontSize=size+'px';status.textContent=size+'px';});})();
