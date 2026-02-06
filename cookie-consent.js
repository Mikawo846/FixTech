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
        
        // Add styles - ЦЕНТРИРОВАННЫЙ ДИЗАЙН ДЛЯ ВСЕХ УСТРОЙСТВ
        banner.style.cssText = `
            position: fixed !important;
            bottom: 20px !important;
            left: 50% !important;
            right: auto !important;
            top: auto !important;
            transform: translateX(-50%) translateY(100%) !important;
            background: #ffffff !important;
            color: #333333 !important;
            padding: 20px 25px !important;
            z-index: 999999 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: space-between !important;
            border-radius: 12px !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2) !important;
            font-size: 14px !important;
            line-height: 1.4 !important;
            width: auto !important;
            max-width: 90vw !important;
            min-width: 300px !important;
            max-width: 600px !important;
            opacity: 0 !important;
            visibility: hidden !important;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
            margin: 0 !important;
            border: 1px solid rgba(0, 0, 0, 0.1) !important;
            box-sizing: border-box !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
            float: none !important;
            clear: both !important;
            overflow: hidden !important;
            contain: layout style !important;
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
        `;

        // Add button styles directly to ensure consistency
        const style = document.createElement('style');
        style.textContent = `
            /* Base styles - центрированный баннер */
            #cookie-banner {
                position: fixed !important;
                bottom: 20px !important;
                left: 50% !important;
                right: auto !important;
                transform: translateX(-50%) translateY(100%) !important;
                background: #ffffff !important;
                color: #333333 !important;
                padding: 20px 25px !important;
                z-index: 999999 !important;
                display: flex !important;
                align-items: center !important;
                justify-content: space-between !important;
                border-radius: 12px !important;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2) !important;
                font-size: 14px !important;
                line-height: 1.4 !important;
                width: auto !important;
                max-width: 90vw !important;
                min-width: 300px !important;
                max-width: 600px !important;
                opacity: 0 !important;
                visibility: hidden !important;
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
                margin: 0 !important;
                border: 1px solid rgba(0, 0, 0, 0.1) !important;
                box-sizing: border-box !important;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
                float: none !important;
                clear: both !important;
                overflow: hidden !important;
                contain: layout style !important;
                backdrop-filter: blur(10px) !important;
                -webkit-backdrop-filter: blur(10px) !important;
            }
            
            #cookie-banner.show {
                opacity: 1 !important;
                visibility: visible !important;
                transform: translateX(-50%) translateY(0) !important;
            }
            
            #cookie-banner .cookie-banner__text {
                flex: 1 !important;
                margin-right: 15px !important;
                color: #333333 !important;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
                font-size: 14px !important;
                line-height: 1.4 !important;
                min-width: 0 !important;
                overflow-wrap: break-word !important;
                word-wrap: break-word !important;
                word-break: break-word !important;
                hyphens: auto !important;
            }
            
            #cookie-banner .cookie-banner__text a {
                color: #4caf50 !important;
                text-decoration: underline !important;
                font-weight: 500 !important;
            }
            
            #cookie-banner .cookie-banner__text a:hover {
                color: #45a049 !important;
            }
            
            #cookie-banner .cookie-banner__buttons {
                flex-shrink: 0 !important;
                min-width: fit-content !important;
            }
            
            #cookie-banner button.cookie-btn {
                background: #4caf50 !important;
                color: white !important;
                border: none !important;
                border-radius: 6px !important;
                padding: 10px 20px !important;
                font-size: 14px !important;
                font-weight: 600 !important;
                cursor: pointer !important;
                transition: all 0.3s ease !important;
                box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3) !important;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
                letter-spacing: 0.3px !important;
                white-space: nowrap !important;
                text-transform: none !important;
                min-height: 40px !important;
                box-sizing: border-box !important;
                max-width: none !important;
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
            
            /* Адаптивные стили для мобильных устройств */
            @media (max-width: 768px) {
                #cookie-banner {
                    bottom: 10px !important;
                    left: 50% !important;
                    right: auto !important;
                    transform: translateX(-50%) translateY(100%) !important;
                    padding: 15px 20px !important;
                    flex-direction: column !important;
                    text-align: center !important;
                    max-width: 95vw !important;
                    min-width: 280px !important;
                    border-radius: 10px !important;
                }
                
                #cookie-banner.show {
                    transform: translateX(-50%) translateY(0) !important;
                }
                
                #cookie-banner .cookie-banner__text {
                    margin-right: 0 !important;
                    margin-bottom: 12px !important;
                    font-size: 13px !important;
                    line-height: 1.3 !important;
                    text-align: center !important;
                }
                
                #cookie-banner button.cookie-btn {
                    width: 100% !important;
                    max-width: 200px !important;
                    min-height: 44px !important;
                    font-size: 15px !important;
                }
            }
            
            @media (max-width: 480px) {
                #cookie-banner {
                    bottom: 8px !important;
                    left: 50% !important;
                    right: auto !important;
                    transform: translateX(-50%) translateY(100%) !important;
                    padding: 12px 16px !important;
                    max-width: 98vw !important;
                    min-width: 260px !important;
                    border-radius: 8px !important;
                }
                
                #cookie-banner.show {
                    transform: translateX(-50%) translateY(0) !important;
                }
                
                #cookie-banner .cookie-banner__text {
                    font-size: 12px !important;
                    margin-bottom: 10px !important;
                    padding: 0 5px !important;
                    line-height: 1.3 !important;
                }
                
                #cookie-banner button.cookie-btn {
                    min-height: 48px !important;
                    font-size: 16px !important;
                    padding: 12px 16px !important;
                }
            }
            
            /* Очень маленькие экраны */
            @media (max-width: 320px) {
                #cookie-banner {
                    bottom: 5px !important;
                    left: 50% !important;
                    right: auto !important;
                    transform: translateX(-50%) translateY(100%) !important;
                    padding: 10px 12px !important;
                    max-width: 99vw !important;
                    min-width: 240px !important;
                }
                
                #cookie-banner.show {
                    transform: translateX(-50%) translateY(0) !important;
                }
                
                #cookie-banner .cookie-banner__text {
                    font-size: 11px !important;
                    line-height: 1.2 !important;
                    margin-bottom: 8px !important;
                }
                
                #cookie-banner button.cookie-btn {
                    font-size: 14px !important;
                    padding: 10px 14px !important;
                    min-height: 44px !important;
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
                console.log('Banner should now be visible and centered');
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
                banner.style.transform = 'translateX(-50%) translateY(100%)';
            }, 300);
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
