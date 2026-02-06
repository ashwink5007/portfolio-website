import { Heart } from "lucide-react";

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="py-8 bg-foreground text-background">
      <div className="container mx-auto px-6">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-sm text-background/70">
            © {currentYear} Alagar Ashwin K. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
