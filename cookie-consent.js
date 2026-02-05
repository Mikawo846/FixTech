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

    // Show cookie banner
    function showCookieBanner() {
        const banner = document.getElementById('cookie-banner');
        if (banner) {
            banner.classList.remove('hidden');
        }
    }

    // Hide cookie banner
    function hideCookieBanner() {
        const banner = document.getElementById('cookie-banner');
        if (banner) {
            banner.classList.add('hidden');
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
        const consent = getCookie('cookie_consent');
        
        if (consent === 'all') {
            // User has already consented, load analytics
            loadAnalytics();
        } else {
            // No consent found, show banner
            showCookieBanner();
        }

        // Add event listener to accept button
        const acceptButton = document.getElementById('cookie-accept');
        if (acceptButton) {
            acceptButton.addEventListener('click', handleCookieConsent);
        }
    }

    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initCookieConsent);
    } else {
        initCookieConsent();
    }
})();
