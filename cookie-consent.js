// Cookie Consent and Analytics Management
(function() {
    'use strict';

    // Cookie functions
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }

    function setCookie(name, value, days) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        const expires = `expires=${date.toUTCString()}`;
        document.cookie = `${name}=${value};${expires};path=/`;
    }

    // Load analytics scripts dynamically
    function loadAnalytics() {
        console.log('Loading analytics scripts...');
        
        // Load Yandex.Metrika
        (function(m,e,t,r,i,k,a){
            m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
            m[i].l=1*new Date();
            for (var j = 0; j < document.scripts.length; j++) {if (document.scripts[j].src === r) { return; }}
            k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)
        })(window, document, 'script', 'https://mc.yandex.ru/metrika/tag.js?id=106225686', 'ym');

        ym(106225686, 'init', {
            ssr: true, 
            webvisor: true, 
            clickmap: true, 
            ecommerce: "dataLayer", 
            accurateTrackBounce: true, 
            trackLinks: true
        });

        // Load Google Analytics
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'G-YE88Y994NX', { 
            anonymize_ip: true 
        });

        // Load Google Analytics script
        const gaScript = document.createElement('script');
        gaScript.async = true;
        gaScript.src = 'https://www.googletagmanager.com/gtag/js?id=G-YE88Y994NX';
        document.head.appendChild(gaScript);

        console.log('Analytics scripts loaded successfully');
    }

    // Create cookie banner dynamically
    function createCookieBanner() {
        // Check if banner already exists
        if (document.getElementById('cookie-banner')) {
            return;
        }

        const banner = document.createElement('div');
        banner.id = 'cookie-banner';
        banner.className = 'cookie-banner hidden';
        banner.innerHTML = `
            <div class="cookie-banner__text">
                На сайте repairo.ru используются файлы cookie для статистики и улучшения работы сайта.
                Продолжая пользоваться сайтом, вы соглашаетесь с использованием cookie.
                Подробнее — в <a href="cookie-agreement.html" target="_blank">Соглашении об использовании файлов cookie</a>.
            </div>
            <div class="cookie-banner__buttons">
                <button id="cookie-accept" class="cookie-btn cookie-btn--primary">Принять</button>
            </div>
        `;
        
        // Add styles
        banner.style.cssText = `
            position: fixed !important;
            bottom: 30px !important;
            left: 50% !important;
            transform: translateX(-50%) translateY(100px) !important;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%) !important;
            color: white !important;
            padding: 20px 25px !important;
            z-index: 99999 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: space-between !important;
            border-radius: 12px !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5) !important;
            font-size: 14px !important;
            line-height: 1.5 !important;
            max-width: 600px !important;
            width: auto !important;
            opacity: 0 !important;
            visibility: hidden !important;
            transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55) !important;
            margin: 0 !important;
        `;

        document.body.appendChild(banner);
    }

    // Show cookie banner
    function showCookieBanner() {
        createCookieBanner(); // Ensure banner exists
        const banner = document.getElementById('cookie-banner');
        if (banner) {
            banner.classList.remove('hidden');
            // Add small delay for smooth animation
            setTimeout(() => {
                banner.classList.add('show');
                // Also update inline styles for maximum compatibility
                banner.style.opacity = '1';
                banner.style.visibility = 'visible';
                banner.style.transform = 'translateX(-50%) translateY(0)';
            }, 100);
        }
    }

    // Hide cookie banner
    function hideCookieBanner() {
        const banner = document.getElementById('cookie-banner');
        if (banner) {
            banner.classList.remove('show');
            // Wait for animation to complete before adding hidden
            setTimeout(() => {
                banner.classList.add('hidden');
                // Also update inline styles for maximum compatibility
                banner.style.opacity = '0';
                banner.style.visibility = 'hidden';
                banner.style.transform = 'translateX(-50%) translateY(100px)';
            }, 400);
        }
    }

    // Handle cookie consent
    function handleCookieConsent() {
        setCookie('cookie_consent', 'all', 365);
        hideCookieBanner();
        loadAnalytics();
    }

    // Initialize cookie consent system
    function initCookieConsent() {
        // Check if user has already given consent
        const hasConsent = getCookie('cookie_consent');
        
        if (!hasConsent) {
            // Show banner only if user hasn't given consent yet
            setTimeout(() => {
                showCookieBanner();
                // Add event listener to accept button after banner is created
                setTimeout(() => {
                    const acceptButton = document.getElementById('cookie-accept');
                    if (acceptButton) {
                        acceptButton.addEventListener('click', handleCookieConsent);
                    }
                }, 100);
            }, 1000);
        } else {
            // User has already consented, load analytics
            loadAnalytics();
        }
    }

    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initCookieConsent);
    } else {
        initCookieConsent();
    }
})();
