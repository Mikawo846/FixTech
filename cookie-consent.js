// Cookie Consent and Analytics Management
(function() {
    'use strict';

    // Cookie functions
    function getCookie(name) {
        try {
            const value = `; ${document.cookie}`;
            const parts = value.split(`; ${name}=`);
            if (parts.length === 2) return parts.pop().split(';').shift();
        } catch (e) {
            console.log('Error reading cookie:', e);
        }
        
        // Fallback to sessionStorage if cookie doesn't exist
        try {
            return sessionStorage.getItem(name);
        } catch (e) {
            console.log('Error reading sessionStorage:', e);
            return null;
        }
    }

    function setCookie(name, value, days) {
        try {
            const date = new Date();
            date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
            const expires = `expires=${date.toUTCString()}`;
            document.cookie = `${name}=${value};${expires};path=/;SameSite=Lax`;
            
            // Verify cookie was set successfully
            const testValue = getCookie(name);
            if (testValue !== value) {
                console.log('Cookie setting failed, possibly incognito mode');
                // Use sessionStorage as fallback for session duration
                try {
                    sessionStorage.setItem(name, value);
                    console.log('Using sessionStorage as fallback');
                } catch (e) {
                    console.log('sessionStorage also not available');
                }
            }
        } catch (e) {
            console.log('Error setting cookie:', e);
            // Try sessionStorage as fallback
            try {
                sessionStorage.setItem(name, value);
                console.log('Using sessionStorage as fallback');
            } catch (e2) {
                console.log('sessionStorage also not available');
            }
        }
    }

    // Load analytics scripts dynamically
    function loadAnalytics() {
        console.log('Loading analytics scripts...');
        
        // Check if we're in incognito/private mode
        try {
            // Test if cookies are enabled
            document.cookie = 'testcookie=1; max-age=60';
            const cookiesEnabled = document.cookie.indexOf('testcookie=') !== -1;
            // Clean up test cookie
            document.cookie = 'testcookie=1; max-age=-1';
            
            if (!cookiesEnabled) {
                console.log('Cookies are disabled, skipping analytics loading');
                return;
            }
        } catch (e) {
            console.log('Error checking cookie availability:', e);
            return;
        }
        
        // Load Yandex.Metrika
        try {
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
        } catch (e) {
            console.log('Failed to load Yandex.Metrika:', e);
        }

        // Load Google Analytics
        try {
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
        } catch (e) {
            console.log('Failed to load Google Analytics:', e);
        }

        console.log('Analytics scripts loading attempted');
    }

    // Create cookie banner dynamically
    function createCookieBanner() {
        console.log('=== CREATE COOKIE BANNER ===');
        
        // Check if banner already exists
        if (document.getElementById('cookie-banner')) {
            console.log('Banner already exists, skipping creation');
            return;
        }

        console.log('Creating new banner element...');
        const banner = document.createElement('div');
        banner.id = 'cookie-banner';
        banner.className = 'cookie-banner';
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
        
        // Add styles - ЕДИНЫЙ ДИЗАЙН ДЛЯ ВСЕХ СТРАНИЦ
        banner.style.cssText = `
            position: fixed !important;
            bottom: 20px !important;
            left: 50% !important;
            right: auto !important;
            top: auto !important;
            transform: translateX(-50%) translateY(100px) !important;
            background: #ffffff !important;
            color: #333333 !important;
            padding: 20px 25px !important;
            z-index: 999999 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: space-between !important;
            border-radius: 16px !important;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15) !important;
            font-size: 14px !important;
            line-height: 1.5 !important;
            max-width: 500px !important;
            width: 90% !important;
            min-width: 280px !important;
            max-height: 80vh !important;
            overflow-y: auto !important;
            opacity: 0 !important;
            visibility: hidden !important;
            transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55) !important;
            margin: 0 !important;
            border: 1px solid rgba(0, 0, 0, 0.1) !important;
            box-sizing: border-box !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
            float: none !important;
            clear: both !important;
        `;

        // Add button styles directly to ensure consistency
        const style = document.createElement('style');
        style.textContent = `
            #cookie-banner .cookie-banner__text {
                flex: 1 !important;
                margin-right: 20px !important;
                color: #333333 !important;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
            }
            
            #cookie-banner .cookie-banner__text a {
                color: #4caf50 !important;
                text-decoration: underline !important;
                font-weight: 500 !important;
            }
            
            #cookie-banner .cookie-banner__text a:hover {
                color: #45a049 !important;
            }
            
            #cookie-banner button.cookie-btn {
                background: #4caf50 !important;
                color: white !important;
                border: none !important;
                border-radius: 8px !important;
                padding: 12px 24px !important;
                font-size: 14px !important;
                font-weight: 600 !important;
                cursor: pointer !important;
                transition: all 0.3s ease !important;
                box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3) !important;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
                letter-spacing: 0.3px !important;
                min-width: 100px !important;
                white-space: nowrap !important;
                text-transform: none !important;
            }
            
            #cookie-banner button.cookie-btn:hover {
                background: #45a049 !important;
                transform: translateY(-1px) !important;
                box-shadow: 0 4px 12px rgba(76, 175, 80, 0.4) !important;
            }
            
            #cookie-banner button.cookie-btn:active {
                transform: translateY(0) !important;
                box-shadow: 0 2px 6px rgba(76, 175, 80, 0.3) !important;
            }
            
            @media (max-width: 768px) {
                #cookie-banner {
                    bottom: 10px !important;
                    left: 5px !important;
                    right: 5px !important;
                    transform: translateY(100px) !important;
                    width: calc(100% - 10px) !important;
                    max-width: none !important;
                    flex-direction: column !important;
                    text-align: center !important;
                    padding: 18px 15px !important;
                    min-height: auto !important;
                    border-radius: 12px !important;
                }
                
                #cookie-banner .cookie-banner__text {
                    margin-right: 0 !important;
                    margin-bottom: 15px !important;
                    font-size: 13px !important;
                    line-height: 1.4 !important;
                    flex: none !important;
                }
                
                #cookie-banner .cookie-banner__buttons {
                    width: 100% !important;
                    display: flex !important;
                    justify-content: center !important;
                }
                
                #cookie-banner button.cookie-btn {
                    width: 100% !important;
                    max-width: 280px !important;
                    min-height: 44px !important;
                    font-size: 14px !important;
                    padding: 12px 20px !important;
                }
            }
            
            @media (max-width: 480px) {
                #cookie-banner {
                    bottom: 5px !important;
                    left: 3px !important;
                    right: 3px !important;
                    width: calc(100% - 6px) !important;
                    padding: 15px 12px !important;
                    border-radius: 8px !important;
                }
                
                #cookie-banner .cookie-banner__text {
                    font-size: 12px !important;
                    margin-bottom: 12px !important;
                }
                
                #cookie-banner button.cookie-btn {
                    min-height: 48px !important;
                    font-size: 15px !important;
                    font-weight: 600 !important;
                }
            }
        `;
        document.head.appendChild(style);

        console.log('Banner created, appending to body...');
        document.body.appendChild(banner);
        console.log('Banner appended to body');
    }

    // Show cookie banner
    function showCookieBanner() {
        console.log('=== SHOW COOKIE BANNER ===');
        createCookieBanner(); // Ensure banner exists
        const banner = document.getElementById('cookie-banner');
        console.log('Banner element found:', !!banner);
        
        if (banner) {
            console.log('Banner element:', banner);
            console.log('Banner styles:', banner.style.cssText);
            
            // Add small delay for smooth animation
            setTimeout(() => {
                banner.classList.add('show');
                // Also update inline styles for maximum compatibility
                banner.style.opacity = '1';
                banner.style.visibility = 'visible';
                banner.style.transform = 'translateX(-50%) translateY(0)';
                console.log('Banner should now be visible');
            }, 100);
        } else {
            console.error('Banner element NOT found after creation!');
        }
    }

    // Hide cookie banner
    function hideCookieBanner() {
        const banner = document.getElementById('cookie-banner');
        if (banner) {
            banner.classList.remove('show');
            // Wait for animation to complete before removing
            setTimeout(() => {
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
        console.log('=== COOKIE CONSENT INITIALIZATION ===');
        console.log('Current URL:', window.location.href);
        console.log('Document readyState:', document.readyState);
        
        // Check if user has already given consent
        const hasConsent = getCookie('cookie_consent');
        console.log('Cookie consent status:', hasConsent);
        console.log('All cookies:', document.cookie);
        
        if (!hasConsent) {
            // Show banner only if user hasn't given consent yet
            console.log('No consent found, showing banner...');
            
            // Use multiple fallback methods to ensure banner shows
            setTimeout(() => {
                console.log('Attempting to show banner...');
                showCookieBanner();
                
                // Add event listener to accept button after banner is created
                setTimeout(() => {
                    const acceptButton = document.getElementById('cookie-accept');
                    if (acceptButton) {
                        console.log('Accept button found, adding listener...');
                        acceptButton.addEventListener('click', handleCookieConsent);
                    } else {
                        console.error('Accept button not found!');
                        // Retry once more
                        setTimeout(() => {
                            const retryButton = document.getElementById('cookie-accept');
                            if (retryButton) {
                                retryButton.addEventListener('click', handleCookieConsent);
                            }
                        }, 500);
                    }
                }, 100);
            }, 1500); // Increased delay to ensure DOM is ready
        } else {
            console.log('Consent already given, loading analytics...');
            // User has already consented, load analytics
            loadAnalytics();
        }
    }

    // Wait for DOM to be ready with multiple fallback methods
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initCookieConsent);
    } else {
        // DOM already loaded, initialize immediately
        initCookieConsent();
    }
    
    // Глобальная функция для тестирования - сбросить куки и показать баннер
    window.resetCookieBanner = function() {
        // Удаляем cookie
        document.cookie = 'cookie_consent=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
        // Удаляем sessionStorage
        try {
            sessionStorage.removeItem('cookie_consent');
        } catch (e) {}
        // Показываем баннер
        showCookieBanner();
        console.log('Cookie banner reset and shown');
    };
    
    // Additional fallback for slow-loading pages
    window.addEventListener('load', function() {
        // Double-check if banner should be shown
        setTimeout(() => {
            const hasConsent = getCookie('cookie_consent');
            const banner = document.getElementById('cookie-banner');
            if (!hasConsent && !banner) {
                console.log('Fallback: Banner not found, retrying...');
                initCookieConsent();
            }
        }, 2000);
    });

})();
