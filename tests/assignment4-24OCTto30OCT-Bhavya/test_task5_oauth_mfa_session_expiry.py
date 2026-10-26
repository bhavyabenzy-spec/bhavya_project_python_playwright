
import pytest
from playwright.async_api import expect


@pytest.mark.asyncio
async def test_oauth_mfa_and_session_expiry(async_page):
    page = async_page
    app_url = "https://demo-app.test"

    # Simulate a small application for testing.
    # This is not a real OAuth provider or a real MFA service.
    async def mock_application(route):
        request = route.request
        url = request.url
        cookies = request.headers.get("cookie", "")

        if url.endswith("/dashboard"):
            if "session=valid" in cookies:
                await route.fulfill(
                    status=200,
                    content_type="text/html",
                    body="""
                        <h1>Dashboard</h1>
                        <button id="view-profile">
                            View Profile
                        </button>
                        <p id="profile-result"></p>
                        <script>
                            document.querySelector(
                                '#view-profile'
                            ).onclick = () => {
                                document.querySelector(
                                    '#profile-result'
                                ).textContent = 'Profile loaded';
                            };
                        </script>
                    """
                )
            else:
                # Simulate an expired or missing session.
                await route.fulfill(
                    status=302,
                    headers={"Location": f"{app_url}/login"}
                )

        elif url.endswith("/login"):
            await route.fulfill(
                status=200,
                content_type="text/html",
                body="""
                    <h1>Login</h1>
                    <input id="username" placeholder="Username">
                    <button id="continue">Continue</button>
                    <script>
                        document.querySelector('#continue').onclick =
                            () => window.location.href = '/mfa';
                    </script>
                """
            )

        elif url.endswith("/mfa"):
            await route.fulfill(
                status=200,
                content_type="text/html",
                body="""
                    <h1>Simulated MFA</h1>
                    <input id="otp" placeholder="Test code">
                    <button id="verify">Verify</button>
                    <p id="message"></p>
                    <script>
                        document.querySelector('#verify').onclick = () => {
                            const code =
                                document.querySelector('#otp').value;

                            if (code === '123456') {
                                document.cookie =
                                    'session=valid; path=/; SameSite=Lax';
                                window.location.href = '/dashboard';
                            } else {
                                document.querySelector(
                                    '#message'
                                ).textContent = 'Invalid test code';
                            }
                        };
                    </script>
                """
            )

        else:
            await route.fulfill(status=404, body="Not found")

    # Route all application requests to our simulated application.
    await page.route("https://demo-app.test/**", mock_application)

    # STEP 1: Try to open the dashboard without a session.
    await page.goto(f"{app_url}/dashboard")

    # The application should redirect us to the login page.
    await expect(page).to_have_url(f"{app_url}/login")
    await expect(
        page.get_by_role("heading", name="Login")
    ).to_be_visible()

    print("Step 1: Unauthenticated access redirected to login.")

    # STEP 2: Enter a test username and continue to simulated MFA.
    await page.locator("#username").fill("test_user")
    await page.locator("#continue").click()

    await expect(page).to_have_url(f"{app_url}/mfa")
    await expect(
        page.get_by_role("heading", name="Simulated MFA")
    ).to_be_visible()

    print("Step 2: Simulated MFA step opened.")

    # STEP 3: Enter the simulated test code.
    # This is a hard-coded demo code, not a real OTP or secret.
    await page.locator("#otp").fill("123456")
    await page.locator("#verify").click()

    await expect(page).to_have_url(f"{app_url}/dashboard")
    await expect(
        page.get_by_role("heading", name="Dashboard")
    ).to_be_visible()

    print("Step 3: Simulated authentication succeeded.")

    # STEP 4: Perform a safe, read-only action.
    await page.locator("#view-profile").click()
    await expect(
        page.locator("#profile-result")
    ).to_have_text("Profile loaded")

    print("Step 4: Read-only profile action succeeded.")

    # STEP 5: Simulate session expiry by removing the session cookie.
    await page.context.clear_cookies()

    # Try accessing the dashboard again.
    await page.goto(f"{app_url}/dashboard")

    # The application should redirect the user to login again.
    await expect(page).to_have_url(f"{app_url}/login")

    print("Step 5: Expired session redirected to login.")

    # STEP 6: Re-authenticate through the approved simulated flow.
    await page.locator("#username").fill("test_user")
    await page.locator("#continue").click()

    await expect(page).to_have_url(f"{app_url}/mfa")

    await page.locator("#otp").fill("123456")
    await page.locator("#verify").click()

    await expect(page).to_have_url(f"{app_url}/dashboard")
    await expect(
        page.get_by_role("heading", name="Dashboard")
    ).to_be_visible()

    print("Step 6: Session restored through the simulated login flow.")

    # Retry the safe, read-only action after re-authentication.
    await page.locator("#view-profile").click()

    await expect(
        page.locator("#profile-result")
    ).to_have_text("Profile loaded")

    print("Task 5: OAuth/MFA simulation and session expiry verified.")
