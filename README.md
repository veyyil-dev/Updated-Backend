# Backend Setup for Vercel Deployment

This guide explains how to set up environment variables for your Flask application when deploying to Vercel.

## Local Development

For local development, use the `.env` file in the root directory of the backend folder. This file contains all the necessary environment variables.

## Vercel Deployment

When deploying to Vercel, you need to set up environment variables in the Vercel dashboard:

1. Log in to your Vercel account
2. Select your project
3. Go to the "Settings" tab
4. Click on "Environment Variables" in the left sidebar
5. Add the following environment variables:

| Variable Name | Value |
|---------------|-------|
| DATABASE_URL | postgres://neondb_owner:npg_js3X0AMyPHCq@ep-gentle-bar-a1814m6n-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require |
| SECRET_KEY | UserAdmin |
| CORS_ORIGINS | * |
| API_HOST | 0.0.0.0 |
| API_PORT | 5000 |
| JWT_EXPIRATION_DELTA | 86400 |

6. Click "Save" to apply the changes
7. Redeploy your application

## Troubleshooting

If you encounter issues with environment variables:

1. Check the Vercel deployment logs for any errors
2. Verify that all environment variables are correctly set in the Vercel dashboard
3. Make sure the environment variables are being used correctly in your code

## Important Notes

- Never commit sensitive information like database credentials to your repository
- The `.env` file is included in `.gitignore` to prevent accidental commits
- For production, consider using more secure values for `SECRET_KEY` 