window.addEventListener('DOMContentLoaded', event => {

    // Navbar shrink function
    var navbarShrink = function () {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) {
            return;
        }
        if (window.scrollY === 0) {
            navbarCollapsible.classList.remove('navbar-shrink');
        } else {
            navbarCollapsible.classList.add('navbar-shrink');
        }
    };

    // This is a more modern approach than the jQuery version, 
    // but the Bootstrap data-attributes in the HTML do most of the work now.
    // This just adds a visual shrink effect not included in the standard scrollspy.
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            offset: 80, // Adjust offset to highlight nav link at the right time
        });
    };

    // Visitor Counter Function
    function visitorCount() {
        // The fetch logic is perfect. No changes needed here.
        fetch('https://yc1mkn35qf.execute-api.us-east-1.amazonaws.com/Prod/put')
            .then(() => fetch('https://yc1mkn35qf.execute-api.us-east-1.amazonaws.com/Prod/get'))
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then((data) => {
                // Check if the element exists before trying to set its innerText
                const visitorElement = document.getElementById('replaceme');
                if (visitorElement) {
                    visitorElement.innerText = data.visitor_count;
                }
            })
            .catch(error => {
                console.error('Error fetching visitor count:', error);
                const visitorElement = document.getElementById('replaceme');
                if (visitorElement) {
                    visitorElement.innerText = 'N/A';
                }
            });
    }

    // Call the function to get the visitor count
    visitorCount();

});