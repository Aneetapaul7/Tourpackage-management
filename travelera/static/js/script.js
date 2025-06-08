// main.js - JavaScript for Travel Website Django Project

// Wait for document to be ready
$(document).ready(function() {

    // Smooth scrolling for navigation links
    $('a[href^="#"]').on('click', function(event) {
        var target = $(this.getAttribute('href'));
        if( target.length ) {
            event.preventDefault();
            $('html, body').stop().animate({
                scrollTop: target.offset().top - 70
            }, 1000);
        }
    });

    // Form submission handler
    $('form').on('submit', function(e) {
        e.preventDefault();
        alert('Thank you for your message! We will get back to you soon.');
        this.reset();
    });

    // Auto-play carousel with settings
    $('#galleryCarousel').carousel({
        interval: 5000,
        ride: 'carousel'
    });

    // Initialize other components if needed
    initializeComponents();
});

// Navbar background change on scroll
$(window).scroll(function() {
    if ($(window).scrollTop() > 50) {
        $('.navbar').addClass('scrolled');
    } else {
        $('.navbar').removeClass('scrolled');
    }
});

// Function to initialize additional components
function initializeComponents() {
    // Add any additional initialization code here
    console.log('Travel website components initialized');
}

// Additional utility functions for Django integration

// CSRF Token helper for Django AJAX requests
function getCSRFToken() {
    return $('[name=csrfmiddlewaretoken]').val();
}

// Enhanced form submission with Django CSRF support
function submitContactForm(formData, csrfToken) {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrfToken);
            }
        }
    });

    $.ajax({
        url: '/contact/',  // Update this to match your Django URL
        type: 'POST',
        data: formData,
        success: function(response) {
            alert('Thank you for your message! We will get back to you soon.');
            $('form')[0].reset();
        },
        error: function(xhr, status, error) {
            alert('Sorry, there was an error sending your message. Please try again.');
            console.error('Form submission error:', error);
        }
    });
}

// Improved form handler for Django
function handleDjangoForm() {
    $('form').off('submit').on('submit', function(e) {
        e.preventDefault();

        var formData = new FormData(this);
        var csrfToken = getCSRFToken();

        if (csrfToken) {
            // If CSRF token is available, submit via AJAX
            submitContactForm(formData, csrfToken);
        } else {
            // Fallback to simple alert if no CSRF token
            alert('Thank you for your message! We will get back to you soon.');
            this.reset();
        }
    });
}

// Gallery image modal functionality (optional enhancement)
function initializeGalleryModal() {
    $('.gallery-item').on('click', function() {
        var imgSrc = $(this).find('img').attr('src');
        var imgAlt = $(this).find('img').attr('alt');

        // Create modal HTML dynamically
        var modalHTML = `
            <div class="modal fade" id="imageModal" tabindex="-1" role="dialog">
                <div class="modal-dialog modal-lg" role="document">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">${imgAlt}</h5>
                            <button type="button" class="close" data-dismiss="modal">
                                <span>&times;</span>
                            </button>
                        </div>
                        <div class="modal-body text-center">
                            <img src="${imgSrc}" class="img-fluid" alt="${imgAlt}">
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Remove existing modal and add new one
        $('#imageModal').remove();
        $('body').append(modalHTML);
        $('#imageModal').modal('show');
    });
}

// Navbar mobile menu improvements
function improveMobileMenu() {
    $('.navbar-toggler').on('click', function() {
        $(this).toggleClass('active');
    });

    // Close mobile menu when clicking on a link
    $('.navbar-nav .nav-link').on('click', function() {
        if ($(window).width() < 992) {
            $('.navbar-collapse').collapse('hide');
            $('.navbar-toggler').removeClass('active');
        }
    });
}

// Loading animation (optional)
function showLoading() {
    $('body').append('<div id="loading" class="d-flex justify-content-center align-items-center position-fixed w-100 h-100" style="top:0;left:0;background:rgba(0,0,0,0.5);z-index:9999;"><div class="spinner-border text-primary" role="status"><span class="sr-only">Loading...</span></div></div>');
}

function hideLoading() {
    $('#loading').remove();
}

// Initialize all enhanced features
$(document).ready(function() {
    handleDjangoForm();
    initializeGalleryModal();
    improveMobileMenu();
});

// Export functions for potential module use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        getCSRFToken,
        submitContactForm,
        showLoading,
        hideLoading,
        initializeComponents
    };
}

// new

document.addEventListener('DOMContentLoaded', function() {
    var carousel = new bootstrap.Carousel(document.getElementById('adventureCarousel'), {
        interval: 2000,
        wrap: true,
        pause: false
    });
});

  window.addEventListener('scroll', function () {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 10) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  });
