**Updated and effective: October 16, 2026**\
**Developer / operator: 韩月 (Han Yue)**\
**Support and privacy: [hanr6969@gmail.com](mailto:hanr6969@gmail.com)**

This policy covers the 现场活动拍摄 app and its product support pages. Ordinary users do not register an app account. The app does not integrate advertising tracking or third-party user behavior analytics SDKs. Its interface is currently in Simplified Chinese.

## 1. Photos and on-device processing

Ordinary photos, Live Photo clips, sound, event text, logos and personal templates are processed and stored on your device. **They are not automatically uploaded to the developer's servers.** Face landmarks are used locally for real-time beauty and makeup rendering, not personal identification or a cloud face database, and are not sent to template or asset services.

You can save results to Apple Photos or export them to an app you choose using system sharing. iCloud Photos and receiving apps process those copies according to your settings and their policies. The app does not provide cloud photo backup, and the developer cannot restore local photos from a server.

## 2. System permissions

- **Camera:** capture and live preview.
- **Add Photos:** save results to Apple Photos. Broader photo-library permission is requested only when you choose to also delete corresponding system photos created by the app.
- **Microphone:** record sound for Live Photos when that feature is enabled; ordinary still capture does not record audio for that reason.
- **Selected images or files:** a system picker lets you choose a logo or image to import.

Manage permissions in iOS Settings. Denial affects the relevant feature; it does not cause photos to be uploaded instead. Ordinary capture does not request location permission.

## 3. Template and optional asset requests

The app uses HTTPS to access a Supabase-hosted template catalog, beauty configuration and asset catalog. Fonts or filter resources are downloaded when you choose to install them. These requests do not include ordinary photos, Live Photo content, event titles, your logo or local face landmarks.

To deliver the connection, diagnose failures and maintain security, the hosting provider may process IP addresses, request times, interface or asset paths, headers, responses and errors. A download request reveals the requested asset path. This information is not used by this app for advertising or user profiling.

The app does not implement an additional remote capture-behavior log. Hosting connection logs may be retained by the provider; we do not promise their immediate deletion after a request. Retention and infrastructure locations depend on the service arrangements and actual configuration. Contact the privacy email for access or deletion requests so we can check the data involved and the available handling options.

See [Supabase's Privacy Policy](https://supabase.com/privacy) and [Data Processing Addendum](https://supabase.com/legal/customer-resources/data-processing-addendum). These links do not imply that ordinary capture content is sent to Supabase. Built-in and cached content remains usable offline.

## 4. Free-event allowance and local preferences

The app stores allowance data in a local file and device Keychain: related event ID, first locally saved record ID, use time, rules version and necessary recovery state. This records the free event, prevents event deletion from returning the allowance and recovers interrupted state. Records are not sent to the developer, linked to advertising identifiers or synchronized at Apple-account level.

The Keychain record uses **ThisDeviceOnly** protection. Deleting an event does not reset the allowance. Uninstalling normally removes sandbox data, but Keychain records may survive reinstalling; a reinstall therefore does not guarantee a reset. Device replacement or migration does not guarantee allowance synchronization.

Capture preferences, guidance completion and the counts and dates of membership or rating prompts stay on the device to remember choices and limit prompts. Local frame timing is used for capture and image processing, not remote usage analytics.

## 5. Apple purchases

Apple handles payment, subscriptions and refunds. The app uses StoreKit's verified product and transaction status, including validity, revocation and upgrades, to determine Pro access. It does not receive your bank-card details or Apple Account password.

Use Restore Purchases with the original purchasing Apple Account to verify valid access. Manage cancellation in Apple's subscription settings. Uninstalling does not cancel a subscription. Apple's processing is covered by [Apple's Privacy Policy](https://www.apple.com/legal/privacy/).

## 6. Authorized template administrators

A whitelist-only studio lets authorized administrators maintain system templates; ordinary users are not offered public registration. When an administrator signs in, email and password are sent over HTTPS to Supabase authentication. Tokens and necessary session details are held in the device Keychain. Signing out clears the app's saved session, not the backend account or published templates.

When an administrator actively saves or publishes a template, its name, description, category, text, logo, template content and necessary version information are sent to the backend to maintain and distribute system templates. Published templates can be downloaded by others. Ordinary capture photos and local photo archives are not included in this publishing action.

Administrator accounts are retained while needed for authorized maintenance. Drafts and published templates are retained while needed to maintain and provide templates or handle related disputes. Contact the privacy email to request removal of authorization, account data or a template. We verify identity and permissions, then handle content that can be deleted. Withdrawing a published template cannot remove copies already downloaded or exported by others. Data required for security, disputes or legal obligations is retained only for those purposes. The app does not promise an unavailable self-service deletion feature.

## 7. Retention, deletion and your requests

Local photos and personal templates stay on the device until you delete them, remove the relevant data or uninstall. Deleting a photo can remove only its app copy or, with system permission, its corresponding Apple Photos copy. Manage iCloud, Recently Deleted and shared copies in the relevant service.

The allowance is separate from photos and events and is retained to maintain used eligibility. Deleting those items does not delete the allowance record. The developer cannot remotely read or erase device-local allowance data. Email us for device-side handling options and their effects. Handling a privacy request does not grant another free event.

If you voluntarily email contact details, a problem description, logs or screenshots, we use them to handle the request and necessary follow-up. We retain them for that purpose and necessary security, dispute or legal requirements. You may request access, correction or deletion. Identity verification may be needed, and handling is subject to legal obligations and the provider's actual capabilities; we do not promise immediate removal of system copies outside our control.

Do not send passwords, verification codes, full payment details or unrelated private photos. Export important photos before uninstalling; reinstallation cannot guarantee recovery of unexported local content.

## 8. Support pages and external links

These static product pages do not run analytics, advertising or tracking scripts, set identifying cookies or load third-party fonts. GitHub Pages hosts them and may process visitor IP addresses and technical request information to serve the site. See [GitHub's Privacy Statement](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement).

An email link opens your own email app. External Apple and Supabase pages have their respective policies.

## 9. Security, updates and contact

Local data uses iOS sandbox and device security mechanisms. Network requests use HTTPS, and administrator sessions are stored in Keychain. These measures reduce risk; they do not guarantee absolute security or permanent preservation. Protect your device and separately back up important photos.

We may update this policy as features or processing change, revise the date and provide appropriate explanations of new purposes or methods. Contact **[hanr6969@gmail.com](mailto:hanr6969@gmail.com)** with policy questions or privacy requests. Ordinary capture does not require registration or submitting identity documents to us.
