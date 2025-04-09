// document.addEventListener("DOMContentLoaded", function () {
//     const toggleButton = document.getElementById("toggleMenu");
//     const menu = document.getElementById("menu");
    
//     // Toggle menu function
//     const toggleMenu = () => {
//         menu.classList.toggle("hidden");
//         menu.classList.toggle("block");
//     };
    
//     // Toggle menu on button click
//     toggleButton.addEventListener("click", toggleMenu);
    
//     // Close menu when clicking outside
//     document.addEventListener("click", (e) => {
//         if (!menu.contains(e.target) && !toggleButton.contains(e.target) && window.innerWidth < 1024) {
//             menu.classList.add("hidden");
//             menu.classList.remove("block");
//         }
//     });
    
//     // Responsive behavior
//     const handleResize = () => {
//         if (window.innerWidth >= 1024) {
//             menu.classList.remove("hidden");
//             menu.classList.add("flex");
//         } else {
//             if (!menu.classList.contains("hidden") && menu.classList.contains("block")) {
//                 menu.classList.add("hidden");
//                 menu.classList.remove("block");
//             }
//             menu.classList.remove("flex");
//         }
//     };
    
//     // Initial check
//     handleResize();
    
//     // Listen for resize events
//     window.addEventListener("resize", handleResize);
    
// });


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
        // Remove existing listeners to prevent duplicates
        button.removeEventListener('click', handleLike);
        button.removeEventListener('touchstart', handleLike);
        
        // Add both click and touchstart for mobile support
        button.addEventListener('click', handleLike);
        button.addEventListener('touchstart', handleLike);
    });
}

async function handleLike(e) {
    // Prevent default for touch events and stop propagation
    if (e.type === 'touchstart') {
        e.preventDefault();
    }
    e.stopPropagation();
    
    const button = e.currentTarget;
    const postId = button.dataset.postId;
    const likeCountElement = button.querySelector('.likes-count');
    const isLiked = button.classList.contains('text-green-600');
    
    // Optimistic UI update
    const currentLikes = parseInt(likeCountElement.textContent);
    likeCountElement.textContent = isLiked ? currentLikes - 1 : currentLikes + 1;
    button.classList.toggle('text-gray-600');
    button.classList.toggle('text-green-600');
    
    // Disable button during request to prevent double-taps
    button.disabled = true;
    
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
        
        if (!data.success) {
            // Revert UI if server request failed
            likeCountElement.textContent = currentLikes;
            button.classList.toggle('text-gray-600');
            button.classList.toggle('text-green-600');
            console.error('Error:', data.error);
        }
    } catch (error) {
        // Revert UI on network error
        likeCountElement.textContent = currentLikes;
        button.classList.toggle('text-gray-600');
        button.classList.toggle('text-green-600');
        console.error('Error:', error);
    } finally {
        // Re-enable button
        button.disabled = false;
    }
}

//Setup copy functionality
function setupCopyButtons() {
    document.querySelectorAll('.copy-btn').forEach(button => {
        button.addEventListener('click', async function() {
            const postId = this.dataset.postId;
            const textToCopy = this.dataset.link;
            const originalText = this.textContent;
            const originalClass = this.className;
            
            // Visual feedback - removed green state
            this.textContent = "Copying...";
            this.disabled = true;
            
            try {
                const copyWithFallback = async () => {
                    try {
                        await navigator.clipboard.writeText(textToCopy);
                        return true;
                    } catch (err) {
                        const textarea = document.createElement('textarea');
                        textarea.value = textToCopy;
                        textarea.style.position = 'fixed';
                        document.body.appendChild(textarea);
                        textarea.select();
                        
                        try {
                            const successful = document.execCommand('copy');
                            document.body.removeChild(textarea);
                            return successful;
                        } catch (fallbackErr) {
                            document.body.removeChild(textarea);
                            return false;
                        }
                    }
                };

                const [copySuccess, postResult] = await Promise.allSettled([
                    copyWithFallback(),
                    fetch('/resources/click_on_copy/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCookie('csrftoken'),
                        },
                        body: JSON.stringify({ post_id: postId })
                    })
                ]);
                
                if (copySuccess.value === true) {
                    this.textContent = "Copied!";
                    showMobileToast("Link copied to clipboard!");
                    
                    // Reset after 1.5 seconds (shorter feedback for success)
                    setTimeout(() => {
                        this.textContent = originalText;
                        this.className = originalClass;
                        this.disabled = false;
                    }, 1500);
                } else {
                    showCopyDialog(textToCopy);
                    this.textContent = "Tap to Copy";
                    this.classList.replace('bg-blue-500', 'bg-gray-600');
                    
                    setTimeout(() => {
                        this.textContent = originalText;
                        this.className = originalClass;
                        this.disabled = false;
                    }, 2000);
                }
                
            } catch (error) {
                console.error('Unexpected error:', error);
                showMobileToast("Failed to copy. Please try again.");
                this.textContent = "Error!";
                this.classList.replace('bg-blue-500', 'bg-red-500');
                
                setTimeout(() => {
                    this.textContent = originalText;
                    this.className = originalClass;
                    this.disabled = false;
                }, 2000);
            }
        });
    });
}

// Rest of your existing helper functions remain unchanged...
// Mobile-friendly dialog for copy fallback
function showCopyDialog(text) {
    const dialog = document.createElement('div');
    dialog.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4';
    dialog.innerHTML = `
        <div class="bg-white rounded-lg p-6 max-w-md w-full">
            <h3 class="text-lg font-bold mb-2">Copy Link</h3>
            <p class="text-gray-700 mb-4">Your browser doesn't support automatic copying.</p>
            <div class="flex items-center border rounded mb-4 p-2 bg-gray-50">
                <input type="text" value="${text}" id="copyInput" 
                       class="flex-1 bg-transparent outline-none" readonly>
                <button onclick="copyFromDialog()" 
                        class="ml-2 px-3 py-1 bg-blue-500 text-white rounded">
                    Copy
                </button>
            </div>
            <button onclick="this.closest('div[class*=\"fixed\"]').remove()" 
                    class="w-full py-2 bg-gray-200 rounded hover:bg-gray-300">
                Close
            </button>
        </div>
    `;
    document.body.appendChild(dialog);
}

// Helper for dialog copy
function copyFromDialog() {
    const input = document.getElementById('copyInput');
    input.select();
    try {
        const successful = document.execCommand('copy');
        showMobileToast(successful ? "Copied!" : "Failed to copy");
    } catch (err) {
        showMobileToast("Failed to copy");
    }
}

// Mobile-friendly toast notification
function showMobileToast(message) {
    const toast = document.createElement('div');
    toast.className = 'fixed bottom-4 left-1/2 transform -translate-x-1/2 bg-gray-800 text-white px-4 py-2 rounded-lg shadow-lg z-50 animate-fadeInOut';
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.classList.add('opacity-0', 'transition-opacity', 'duration-300');
        setTimeout(() => toast.remove(), 300);
    }, 2000);
}

// Add this to your CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeInOut {
        0% { opacity: 0; transform: translate(-50%, 10px); }
        10% { opacity: 1; transform: translate(-50%, 0); }
        90% { opacity: 1; transform: translate(-50%, 0); }
        100% { opacity: 0; transform: translate(-50%, -10px); }
    }
    .animate-fadeInOut {
        animation: fadeInOut 2s ease forwards;
    }
`;
document.head.appendChild(style);






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




function getToastClasses(type) {
    const classes = {
        info: 'bg-blue-50 text-blue-800',
        success: 'bg-green-50 text-green-800',
        error: 'bg-red-50 text-red-800',
        warning: 'bg-yellow-50 text-yellow-800'
    };
    return classes[type] || classes.info;
}

function getToastIconClasses(type) {
    const classes = {
        info: 'text-blue-500',
        success: 'text-green-500',
        error: 'text-red-500',
        warning: 'text-yellow-500'
    };
    const baseClass = 'inline-flex items-center justify-center flex-shrink-0 w-6 h-6';
    return `${baseClass} ${classes[type] || classes.info}`;
}

function dismissToast(toast) {
    toast.style.opacity = '0';
    toast.style.maxHeight = '0';
    setTimeout(() => {
        toast.remove();
        const container = document.getElementById('toast-container');
        if (container && container.children.length === 0) {
            container.remove();
        }
    }, 300);
}

// Add CSS styles (should be in your stylesheet)
const toastStyles = document.createElement('style');
toastStyles.textContent = `
.toast-notification {
    will-change: transform, opacity, max-height;
    transition: opacity 300ms ease, max-height 300ms ease, transform 300ms ease;
}
.toast-icon {
    font-size: 1.25rem;
}
.toast-icon:after {
    content: '';
    display: inline-block;
    width: 1em;
    height: 1em;
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
}
.toast-icon.info:after {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='currentColor'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z' /%3E%3C/svg%3E");
}
.toast-icon.success:after {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='currentColor'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M5 13l4 4L19 7' /%3E%3C/svg%3E");
}
.toast-icon.error:after {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='currentColor'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M6 18L18 6M6 6l12 12' /%3E%3C/svg%3E");
}
.toast-icon.warning:after {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='currentColor'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z' /%3E%3C/svg%3E");
}
`;
document.head.appendChild(toastStyles);












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