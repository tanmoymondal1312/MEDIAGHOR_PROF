
// Navbar
document.addEventListener("DOMContentLoaded", function () {
    let toggleButton = document.getElementById("toggleMenu");
    let menu = document.getElementById("menu");



    toggleButton.addEventListener("click", function () {

        if (menu.classList.contains("hidden")) {
            menu.classList.remove("hidden");
            menu.classList.add("block");
        } else {
            console.log("🙈 Menu is visible. Hiding it.");
            menu.classList.add("hidden");
            menu.classList.remove("block");
        }
    });

    // Ensure visibility on desktop resize
    window.addEventListener("resize", function () {

        if (window.innerWidth >= 1024) {
            menu.classList.remove("hidden");
            menu.classList.add("flex");
        } else {
            menu.classList.add("hidden");
            menu.classList.remove("flex");
        }
    });

    // Debugging when navigating to a new page
    document.addEventListener("visibilitychange", function () {
        if (document.visibilityState === "hidden") {
        } else {
            if (window.innerWidth >= 1024) {
                menu.classList.remove("hidden");
                menu.classList.add("flex");
            }
        }
    });
    if (window.innerWidth >= 1024) {
        menu.classList.remove("hidden");
        menu.classList.add("flex");
    } else {
        menu.classList.add("hidden");
        menu.classList.remove("flex");
    }
});



// Global Card


// Add this new function
document.addEventListener("DOMContentLoaded", () => {
    // Initialize all library content boxes with responsive text sizing
    initLibraryContentBoxes();
    
    // Setup description toggles
    setupDescriptionToggles();
});

function initLibraryContentBoxes() {
    document.querySelectorAll('.library-content').forEach(pre => {
        const container = pre.parentElement;
        let fontSize = 14;
        pre.style.fontSize = `${fontSize}px`;
        
        const adjustTextSize = () => {
            const isOverflowing = () => {
                return pre.scrollHeight > container.clientHeight || 
                       pre.scrollWidth > container.clientWidth;
            };
            
            while (isOverflowing() && fontSize > 8) {
                fontSize -= 0.5;
                pre.style.fontSize = `${fontSize}px`;
            }
            
            if (isOverflowing()) {
                container.classList.add('overflow-x-auto');
                container.classList.remove('overflow-hidden');
                pre.style.whiteSpace = 'pre';
            }
        };
        
        adjustTextSize();
        
        const resizeObserver = new ResizeObserver(() => {
            fontSize = 14;
            pre.style.fontSize = `${fontSize}px`;
            container.classList.remove('overflow-x-auto');
            container.classList.add('overflow-hidden');
            pre.style.whiteSpace = 'pre-wrap';
            adjustTextSize();
        });
        resizeObserver.observe(container);
    });
}

function setupDescriptionToggles() {
    document.querySelectorAll('.toggle-text').forEach(button => {
        button.addEventListener('click', function() {
            const card = this.closest('.library-card-content');
            const shortText = card.querySelector('.short-text');
            const fullText = card.querySelector('.full-text');
            
            shortText.classList.toggle('hidden');
            fullText.classList.toggle('hidden');
            this.textContent = fullText.classList.contains('hidden') ? '..More' : 'Show Less';
        });
    });
}



function copyToClipboard(button) {
    const text = button.getAttribute('data-link');
    navigator.clipboard.writeText(text).then(() => {
        const originalText = button.textContent;
        button.textContent = "Copied!";
        button.classList.remove('bg-gray-600', 'hover:bg-gray-700');
        button.classList.add('bg-green-600', 'hover:bg-green-700');
        
        setTimeout(() => {
            button.textContent = originalText;
            button.classList.remove('bg-green-600', 'hover:bg-green-700');
            button.classList.add('bg-gray-600', 'hover:bg-gray-700');
        }, 1500);
    }).catch(err => {
        console.error("Failed to copy: ", err);
    });
}










