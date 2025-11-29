import { motion } from 'framer-motion';
import { useInView } from 'framer-motion';
import { useRef } from 'react';
import { Code2, Palette, Zap } from 'lucide-react';

const features = [
  {
    icon: Code2,
    title: 'Clean Code',
    description: 'Writing maintainable, scalable, and efficient code that stands the test of time.',
  },
  {
    icon: Palette,
    title: 'Creative Design',
    description: 'Crafting beautiful interfaces that balance aesthetics with functionality.',
  },
  {
    icon: Zap,
    title: 'Performance',
    description: 'Optimizing every detail for lightning-fast load times and smooth interactions.',
  },
];

export const About = () => {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, margin: '-100px' });

  return (
    <section id="about" ref={ref} className="relative py-32 overflow-hidden">
      {/* Background Elements */}
      <div className="absolute top-1/2 left-1/4 w-64 h-64 bg-accent/10 rounded-full blur-[100px]" />
      
      <div className="container mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          animate={isInView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-6xl font-bold mb-6">
            About <span className="text-gradient">Me</span>
          </h2>
          <p className="text-lg md:text-xl text-muted-foreground max-w-3xl mx-auto">
            I’m Ashwin,self-proclaimed vibe coder,
            and AI enthusiast with a soft spot for clean UI and clever UX. 
            I build, break, and rebuild web projects until they finally look and work the way I imagine (or at least stop crashing).
            Aspiring to be a web developer and UI/UX designer, I love blending creativity with logic — from designing interfaces to editing videos and photos that actually make sense. 
            I believe in minimal design, maximum impact, and a dash of sarcasm to keep things real.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 50 }}
              animate={isInView ? { opacity: 1, y: 0 } : {}}
              transition={{ duration: 0.6, delay: index * 0.2 }}
              className="glass p-8 rounded-2xl hover:glow-primary transition-all duration-300 group"
            >
              <div className="w-14 h-14 rounded-xl bg-primary/10 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <feature.icon className="w-7 h-7 text-primary" />
              </div>
              <h3 className="text-2xl font-bold mb-4">{feature.title}</h3>
              <p className="text-muted-foreground">{feature.description}</p>
            </motion.div>
          ))}
        </div>

        <motion.div
          initial={{ opacity: 0, y: 50 }}
          animate={isInView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6, delay: 0.8 }}
          className="glass p-8 md:p-12 rounded-2xl max-w-4xl mx-auto mt-16"
        >
          <h3 className="text-3xl font-bold mb-6">My Journey</h3>
          <div className="space-y-4 text-muted-foreground">
            <p>
              My journey into web development started with a curiosity about how websites work.
              That curiosity quickly evolved into a passion for creating seamless digital experiences
              that push the boundaries of what's possible on the web.
            </p>
            <p>
              Over the years, I've had the privilege of working with startups and established companies,
              helping them bring their visions to life through innovative solutions and cutting-edge
              technologies. Every project is an opportunity to learn, grow, and create something amazing.
            </p>
            <p>
              When I'm not coding, you'll find me exploring new design trends, experimenting with
              emerging technologies, or contributing to open-source projects.
            </p>
          </div>
        </motion.div>
      </div>
    </section>
  );
};
