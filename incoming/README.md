# Publish the approved Rev F Ocean Guardians storefront
Upload **JMS_Merchandise_RevF_Publish_Package.zip** to this `incoming/` folder on the `main` branch using GitHub's **Add file → Upload files** action.

A GitHub Actions workflow will verify the ZIP against the exact approved package checksum, extract four original approved shirt preview crops plus the two reference sheets, replace `merchandise.html`, and commit the results. The ZIP is removed by the workflow after extraction.

The ZIP must be the unmodified file provided in the ChatGPT conversation. If the workflow is disabled or branch permissions block the commit, no publication occurs; check the repository's **Actions** tab.

These are low-resolution *storefront previews*, not transparent, print-ready masters. Printify/Etsy publication and pricing are intentionally not part of this process.
