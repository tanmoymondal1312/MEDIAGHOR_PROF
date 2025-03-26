
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


document.addEventListener("DOMContentLoaded", () => {
    // Initialize all functions
    initLibraryContentBoxes();
    setupDescriptionToggles();
    setupLikeButtons();
    setupCopyButtons();
});

// Text sizing for library content
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

// Toggle description text
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

// Like/Unlike functionality
function setupLikeButtons() {
    document.querySelectorAll('[data-like-button]').forEach(button => {
        button.addEventListener('click', async function() {
            const postId = this.dataset.postId;
            const likeCountElement = this.querySelector('.likes-count');
            const isLiked = this.classList.contains('text-green-600');
            
            try {
                const response = await fetch('/blogs/post-impression/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken'),
                    },
                    body: JSON.stringify({
                        post_id: postId,
                        action: isLiked ? 'unlike' : 'like'
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    likeCountElement.textContent = data.new_likes;
                    this.classList.toggle('text-gray-600');
                    this.classList.toggle('text-green-600');
                } else {
                    console.error('Error:', data.error);
                }
            } catch (error) {
                console.error('Error:', error);
            }
        });
    });
}

// Copy button functionality - Optimized version
function setupCopyButtons() {
    document.querySelectorAll('.copy-btn').forEach(button => {
        button.addEventListener('click', async function() {
            const postId = this.dataset.postId;
            const textToCopy = this.dataset.link;
            const originalText = this.textContent;
            
            // Immediately show visual feedback for the copy action
            this.textContent = "Copying...";
            this.classList.replace('bg-gray-600', 'bg-blue-500');
            this.disabled = true;
            
            try {
                // Execute copy and post in parallel
                const [copyResult, postResult] = await Promise.allSettled([
                    navigator.clipboard.writeText(textToCopy),
                    fetch('/resources/click_on_copy/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCookie('csrftoken'),
                        },
                        body: JSON.stringify({ post_id: postId })
                    })
                ]);
                
                // Handle results
                if (copyResult.status === 'fulfilled') {
                    this.textContent = "Copied!";
                    this.classList.replace('bg-blue-500', 'bg-green-600');
                } else {
                    this.textContent = "Copy Failed!";
                    this.classList.replace('bg-blue-500', 'bg-red-500');
                    console.error('Copy failed:', copyResult.reason);
                }
                
                if (postResult.status === 'fulfilled') {
                    const data = await postResult.value.json();
                    if (data.status !== 'success') {
                        console.error('Post failed:', data.message);
                    }
                } else {
                    console.error('Post request failed:', postResult.reason);
                }
                
            } catch (error) {
                console.error('Error:', error);
                this.textContent = "Error!";
                this.classList.replace('bg-blue-500', 'bg-red-500');
            } finally {
                setTimeout(() => {
                    this.textContent = originalText;
                    this.classList.replace(/bg-(green|red|blue)-\d+/, 'bg-gray-600');
                    this.disabled = false;
                }, 1500);
            }
        });
    });
}

// Enhanced CSRF token helper function
function getCookie(name) {
    // First check for a meta tag (common alternative)
    const metaTag = document.querySelector('meta[name="csrf-token"]');
    if (metaTag) {
        return metaTag.content;
    }
    
    // Fallback to cookie
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Global CSRF setup for all fetch requests
(function() {
    const csrfToken = getCookie('csrftoken');
    if (csrfToken) {
        const originalFetch = window.fetch;
        window.fetch = async function(resource, init = {}) {
            // Add CSRF token to all non-GET requests to same origin
            if (!init.method || init.method.toUpperCase() !== 'GET') {
                const url = typeof resource === 'string' ? resource : resource.url;
                if (url && !url.startsWith('http') || url.startsWith(window.location.origin)) {
                    init.headers = {
                        ...init.headers,
                        'X-CSRFToken': csrfToken
                    };
                }
            }
            return originalFetch(resource, init);
        };
    }
})();