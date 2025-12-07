// import type { NextConfig } from "next";

// const nextConfig: NextConfig = {
//   /* config options here */
// };

// export default nextConfig;





/** @type {import('next').NextConfig} */
const nextConfig = {
  // Add this section to proxy all '/api' requests to the FastAPI backend
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        // Update this URL if your backend is not on localhost:8000
        destination: 'http://localhost:8000/api/:path*', 
      },
    ]
  },
};

module.exports = nextConfig;


