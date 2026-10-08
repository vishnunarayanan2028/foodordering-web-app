function fillDemoCredentials(email, password) {
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    if (emailInput && passwordInput) {
        emailInput.value = email;
        passwordInput.value = password;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const btn = document.getElementById('loginBtn');
            const errorMsg = document.getElementById('errorMsg');
            const email = (document.getElementById('email').value || '').trim();
            const password = document.getElementById('password').value;
            
            try {
                btn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Logging in...';
                btn.disabled = true;
                errorMsg.style.display = 'none';
                
                const res = await ApiClient.post('/auth/login', { email, password });
                if (!res || !res.token) {
                    throw new Error('Invalid login response from server');
                }
                
                ApiClient.setToken(res.token);
                ApiClient.setUser(res.user);
                
                showToast('Login successful!');
                
                // Redirect based on role
                setTimeout(() => {
                    if (res.user.role === 'admin') {
                        window.location.href = '/admin-dashboard.html';
                    } else if (res.user.role === 'restaurant') {
                        window.location.href = '/restaurant-dashboard.html';
                    } else {
                        window.location.href = '/menu.html';
                    }
                }, 800);
            } catch (err) {
                console.error('Login error:', err);
                errorMsg.textContent = err.message || 'Login failed. Please check your credentials.';
                errorMsg.style.display = 'block';
                btn.innerHTML = 'Login';
                btn.disabled = false;
            }
        });
    }
    
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const btn = document.getElementById('registerBtn');
            const errorMsg = document.getElementById('errorMsg');
            
            const name = (document.getElementById('name').value || '').trim();
            const email = (document.getElementById('email').value || '').trim();
            const phone = (document.getElementById('phone').value || '').trim();
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirmPassword').value;
            
            if (password !== confirmPassword) {
                errorMsg.textContent = 'Passwords do not match';
                errorMsg.style.display = 'block';
                return;
            }
            
            try {
                btn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Registering...';
                btn.disabled = true;
                errorMsg.style.display = 'none';
                
                const res = await ApiClient.post('/auth/register', { name, email, phone, password });
                if (!res || !res.token) {
                    throw new Error('Invalid registration response from server');
                }
                ApiClient.setToken(res.token);
                ApiClient.setUser(res.user);
                
                showToast('Registration successful!');
                
                setTimeout(() => {
                    window.location.href = '/menu.html';
                }, 800);
            } catch (err) {
                console.error('Registration error:', err);
                errorMsg.textContent = err.message || 'Registration failed';
                errorMsg.style.display = 'block';
                btn.innerHTML = 'Register';
                btn.disabled = false;
            }
        });
    }
});
