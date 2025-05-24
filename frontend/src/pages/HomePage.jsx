import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Spline from '@splinetool/react-spline';

const HomePage = () => {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate loading time for Spline scene
    const timer = setTimeout(() => {
      setLoading(false);
    }, 2000);
    
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="relative min-h-screen bg-gradient-to-b from-blue-900 to-indigo-900 text-white">
      {/* Loading indicator */}
      {loading && (
        <div className="absolute inset-0 flex items-center justify-center z-10 bg-black bg-opacity-70">
          <div className="text-center">
            <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-white mx-auto"></div>
            <p className="mt-4 text-xl">Loading 3D Experience...</p>
          </div>
        </div>
      )}

      {/* 3D Background with Spline */}
      <div className="absolute inset-0 z-0 opacity-70">
        <Spline 
          scene="https://prod.spline.design/example-scene-id/scene.splinecode" 
          className="w-full h-full"
        />
      </div>

      {/* Content overlay */}
      <div className="relative z-10 container mx-auto px-4 py-16 flex flex-col items-center justify-center min-h-screen">
        <h1 className="text-5xl md:text-7xl font-bold mb-6 text-center">
          FixMyPhone
        </h1>
        <p className="text-xl md:text-2xl mb-12 text-center max-w-3xl">
          Professional phone repair services at your fingertips. Fast, reliable, and hassle-free.
        </p>
        
        <div className="flex flex-col sm:flex-row gap-4 mt-8">
          <Link 
            to="/login" 
            className="bg-white text-indigo-900 hover:bg-indigo-100 px-8 py-3 rounded-full font-semibold text-lg transition-colors"
          >
            Login
          </Link>
          <Link 
            to="/register" 
            className="bg-transparent border-2 border-white hover:bg-white hover:text-indigo-900 px-8 py-3 rounded-full font-semibold text-lg transition-colors"
          >
            Register
          </Link>
        </div>

        <div className="mt-24 grid grid-cols-1 md:grid-cols-3 gap-8 w-full max-w-5xl">
          <div className="bg-white bg-opacity-10 p-6 rounded-xl backdrop-blur-sm">
            <h3 className="text-xl font-semibold mb-3">Quick Repairs</h3>
            <p>Most repairs completed same-day with our expert technicians.</p>
          </div>
          <div className="bg-white bg-opacity-10 p-6 rounded-xl backdrop-blur-sm">
            <h3 className="text-xl font-semibold mb-3">Quality Parts</h3>
            <p>We use only high-quality replacement parts with warranty.</p>
          </div>
          <div className="bg-white bg-opacity-10 p-6 rounded-xl backdrop-blur-sm">
            <h3 className="text-xl font-semibold mb-3">Online Tracking</h3>
            <p>Track your repair status in real-time through our platform.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
