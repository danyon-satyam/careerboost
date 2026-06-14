import { motion } from 'framer-motion';
import CrossGridBackground from '../components/layout/CrossGridBackground';
import { fadeInUp } from '../animations/variants';

function CandidateFormPage() {
  return (
    <div className="relative min-h-screen">
      <CrossGridBackground />
      <motion.div
        className="relative z-10 flex items-center justify-center min-h-screen"
        initial="hidden"
        animate="visible"
        variants={fadeInUp}
      >
        <h1 className="text-5xl font-bold text-white">
          Candidate<span className="gradient-text">Form</span>
        </h1>
      </motion.div>
    </div>
  );
}

export default CandidateFormPage;
