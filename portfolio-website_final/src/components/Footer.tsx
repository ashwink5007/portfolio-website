import { motion } from 'framer-motion';
import { Github, Linkedin, Mail, Heart } from 'lucide-react';
import { Button } from '@/components/ui/button';

export const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="relative border-t border-border/50 py-12">
      <div className="container mx-auto px-4">
        <div className="grid md:grid-cols-3 gap-8 mb-8">
          {/* Brand */}
          <div>
            <h3 className="text-2xl font-bold text-gradient mb-4">Portfolio</h3>
            <p className="text-muted-foreground">
              Crafting immersive digital experiences with passion and precision.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="font-semibold mb-4">Quick Links</h4>
            <ul className="space-y-2">
              {['Home', 'About', 'Projects', 'Skills', 'Contact'].map((item) => (
                <li key={item}>
                  <button
                    onClick={() => {
                      const element = document.querySelector(`#${item.toLowerCase()}`);
                      if (element) {
                        element.scrollIntoView({ behavior: 'smooth' });
                      }
                    }}
                    className="text-muted-foreground hover:text-primary transition-colors"
                  >
                    {item}
                  </button>
                </li>
              ))}
            </ul>
          </div>

          {/* Social Links */}
          <div>
            <h4 className="font-semibold mb-4">Connect</h4>
            <div className="flex gap-4">
              <Button
                size="icon"
                variant="ghost"
                className="glass hover:glow-primary transition-all"
                asChild
              >
                <a href="https://github.com/ashwink5007" target="_blank" rel="noopener noreferrer">
                  <Github className="w-5 h-5" />
                </a>
              </Button>
              <Button
                size="icon"
                variant="ghost"
                className="glass hover:glow-primary transition-all"
                asChild
              >
                <a href="https://www.linkedin.com/in/alagar-ashwin-k-625444283/" target="_blank" rel="noopener noreferrer">
                  <Linkedin className="w-5 h-5" />
                </a>
              </Button>
              <Button
                size="icon"
                variant="ghost"
                className="glass hover:glow-primary transition-all"
                asChild
              >
                <a href="mailto:alagarashwin.k@example.com">
                  <Mail className="w-5 h-5" />
                </a>
              </Button>
            </div>
          </div>
        </div>

        {/* Copyright */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="pt-8 border-t border-border/50 text-center text-muted-foreground flex items-center justify-center gap-2"
        >
          <span>© {currentYear} Portfolio. Made with</span>
          <Heart className="w-4 h-4 text-primary fill-primary animate-pulse" />
          <span>and lots of coffee</span>
        </motion.div>
      </div>
    </footer>
  );
};
