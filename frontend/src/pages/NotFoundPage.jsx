import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { fadeInUp } from '../animations/variants';

function NotFoundPage() {
  return (
    <motion.div
      className="min-h-screen flex flex-col items-center justify-center text-center px-4"
      initial="hidden"
      animate="visible"
      variants={fadeInUp}
    >
      <h1 className="text-6xl font-bold gradient-text mb-4">404</h1>
      <p className="text-gray-400 text-lg mb-8">
        This page doesn't exist.
      </p>
      <Link
        to="/"
        className="px-6 py-3 rounded-full glass-pill text-teal-400 hover:border-teal-400/50 transition-colors"
      >
        Back to home
      </Link>
    </motion.div>
  );
}

export default NotFoundPage;
