/**
 * Shared transition configs for Framer Motion.
 */

export const transitionDefault = {
  duration: 0.3,
  ease: [0.4, 0, 0.2, 1],
};

export const transitionSlow = {
  duration: 0.6,
  ease: [0.4, 0, 0.2, 1],
};

export const transitionFast = {
  duration: 0.15,
  ease: [0.4, 0, 0.2, 1],
};

export const transitionBounce = {
  type: 'spring',
  stiffness: 300,
  damping: 20,
};

export const transitionSmoothSpring = {
  type: 'spring',
  stiffness: 100,
  damping: 15,
};

export const pageTransition = {
  initial: { opacity: 0, y: 12 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -12 },
  transition: transitionDefault,
};
