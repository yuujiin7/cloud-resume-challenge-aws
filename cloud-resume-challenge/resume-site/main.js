$(document).ready(function () {

    const OFFSET_TOP = 150; // Adjust as needed

    function onScroll() {
        var link = $('.navbar a.dot');
        var top = $(window).scrollTop();

        $('.sec').each(function () {
            var id = $(this).attr('id');
            var height = $(this).height();
            var offset = $(this).offset().top - OFFSET_TOP;

            if (top >= offset && top < offset + height) {
                updateActiveClasses(id);
            }
        });
    }

    function updateActiveClasses(id) {
        var link = $('.navbar a.dot');
        var listItem = $('.navbar').find('[data-scroll="' + id + '"]').closest('li');

        link.removeClass('active');
        listItem.find('.dot').addClass('active');
        $('.navbar ul li').removeClass('hovered');
        listItem.addClass('hovered');
    }

    $(window).on('scroll', _.throttle(onScroll, 200));

    function visitorCount() {
        fetch('https://yc1mkn35qf.execute-api.us-east-1.amazonaws.com/Prod/put')
            .then(() => fetch('https://yc1mkn35qf.execute-api.us-east-1.amazonaws.com/Prod/get'))
            .then(response => response.json())
            .then((data) => {
                document.getElementById('replaceme').innerText = data.visitor_count;
            })
            .catch(error => {
                console.error('Error fetching visitor count:', error);
            });
    }
    
    visitorCount();
    
    
    
});
