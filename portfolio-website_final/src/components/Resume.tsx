import { motion, useInView } from 'framer-motion';
import { Download, FileText, Sparkles } from 'lucide-react';
import { Button } from './ui/button';
import { useRef, useEffect, useState } from 'react';

export const Resume = () => {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, margin: "-100px" });
  const [particles, setParticles] = useState<Array<{ id: number; x: number; y: number; size: number; delay: number }>>([]);

  useEffect(() => {
    // Generate random particles around the button
    const newParticles = Array.from({ length: 30 }, (_, i) => ({
      id: i,
      x: Math.random() * 100 - 50,
      y: Math.random() * 100 - 50,
      size: Math.random() * 4 + 2,
      delay: Math.random() * 2,
    }));
    setParticles(newParticles);
  }, []);

  const handleDownload = () => {
    // Create a link element and trigger download
    const link = document.createElement('a');
    link.href = '/Ashwin_CV.pdf';
    link.download = 'Ashwin_CV.pdf';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <section id="resume" className="py-20 relative overflow-hidden">
      <div className="container mx-auto px-4">
        <motion.div
          ref={ref}
          initial={{ opacity: 0, y: 50 }}
          animate={isInView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6 }}
          className="text-center"
        >
          <motion.div
            initial={{ scale: 0 }}
            animate={isInView ? { scale: 1 } : {}}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="inline-block mb-4"
          >
            <FileText className="w-16 h-16 text-primary mx-auto" />
          </motion.div>

          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            animate={isInView ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="text-4xl md:text-5xl font-heading font-bold mb-4"
          >
            Download My <span className="text-gradient">Resume</span>
          </motion.h2>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={isInView ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.5, delay: 0.4 }}
            className="text-lg text-muted-foreground mb-12 max-w-2xl mx-auto"
          >
            Get a comprehensive overview of my experience, skills, and achievements
          </motion.p>

          {/* Animated stats */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={isInView ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.5, delay: 0.5 }}
            className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12 max-w-3xl mx-auto"
          >
          </motion.div>

          {/* Download button with particle animation */}
          <motion.div
            initial={{ scale: 0 }}
            animate={isInView ? { scale: 1 } : {}}
            transition={{ duration: 0.5, delay: 0.9 }}
            className="relative inline-block"
          >
            {/* Particle effects */}
            <div className="absolute inset-0 pointer-events-none">
              {particles.map((particle) => (
                <motion.div
                  key={particle.id}
                  className="absolute top-1/2 left-1/2 rounded-full bg-primary"
                  style={{
                    width: particle.size,
                    height: particle.size,
                  }}
                  animate={{
                    x: [0, particle.x, particle.x * 1.5],
                    y: [0, particle.y, particle.y * 1.5],
                    opacity: [0, 1, 0],
                    scale: [0, 1, 0.5],
                  }}
                  transition={{
                    duration: 3,
                    delay: particle.delay,
                    repeat: Infinity,
                    ease: "easeOut",
                  }}
                />
              ))}
            </div>

            {/* Glow effect */}
            <motion.div
              className="absolute inset-0 rounded-full blur-2xl opacity-50 bg-primary/30"
              animate={{
                scale: [1, 1.2, 1],
                opacity: [0.3, 0.6, 0.3],
              }}
              transition={{
                duration: 2,
                repeat: Infinity,
                ease: "easeInOut",
              }}
            />

            {/* Download button */}
            <Button
              onClick={handleDownload}
              size="lg"
              className="relative z-10 group text-lg px-8 py-6 bg-gradient-to-r from-primary to-accent hover:scale-105 transition-all duration-300 shadow-glow"
            >
              <Download className="mr-2 h-5 w-5 group-hover:animate-bounce" />
              Download Resume
              <Sparkles className="ml-2 h-5 w-5 group-hover:rotate-12 transition-transform" />
            </Button>
          </motion.div>

          {/* Decorative elements */}
          <motion.div
            className="absolute top-1/2 left-1/4 w-32 h-32 rounded-full bg-primary/10 blur-3xl"
            animate={{
              scale: [1, 1.2, 1],
              opacity: [0.3, 0.5, 0.3],
            }}
            transition={{
              duration: 4,
              repeat: Infinity,
              ease: "easeInOut",
            }}
          />
          <motion.div
            className="absolute top-1/2 right-1/4 w-32 h-32 rounded-full bg-accent/10 blur-3xl"
            animate={{
              scale: [1.2, 1, 1.2],
              opacity: [0.5, 0.3, 0.5],
            }}
            transition={{
              duration: 4,
              repeat: Infinity,
              ease: "easeInOut",
            }}
          />
        </motion.div>
      </div>
    </section>
  );
};
