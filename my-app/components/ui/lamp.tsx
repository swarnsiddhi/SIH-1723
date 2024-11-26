"use client";
import React, { useState } from "react";
import { motion } from "framer-motion";
import { useRouter } from "next/router";
import styled from "styled-components";
import axios from "axios";
import { cn } from "@/lib/utils";

// Styled Components
const Navbar = styled.nav`
  position: absolute;
  top: -7rem;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  justify-content: space-around;
  align-items: center;
  width: 90%;
  max-width: 1200px;
  padding: 1rem;
  border-radius: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  z-index: 10;
`;

const NavItem = styled.a`
  color: #fff;
  text-decoration: none;
  font-size: 1rem;
  font-weight: 500;
  transition: color 0.3s ease;

  &:hover {
    color: #e2e8f0;
  }

  @media (min-width: 768px) {
    font-size: 1.2rem;
  }
`;

const InputCard = styled.form`
  margin-top: 2rem;
  width: 100%;
  max-width: 500px;
  padding: 1.5rem;
  background: #ffffff;
  border-radius: 15px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

const InputField = styled.input`
  padding: 0.75rem;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  font-size: 1rem;
  width: 100%;
  outline: none;
  color: gray;
  transition: border-color 0.3s ease;

  &:focus {
    border-color: #64748b;
  }
`;

const SubmitButton = styled.button`
  padding: 0.75rem;
  background: linear-gradient(to right, #64748b, #94a3b8);
  color: #ffffff;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.3s ease;

  &:hover {
    background: linear-gradient(to right, #94a3b8, #64748b);
  }
`;

// Main Component
export default function LampDemo() {
  const [elongation, setElongation] = useState('');
  const [uts, setUts] = useState('');
  const [conductivity, setConductivity] = useState('');
  const router = useRouter();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('/api/save_features', {
        elongation,
        uts,
        conductivity,
      });
      router.push('/results'); // Redirect to the results page
    } catch (error) {
      console.error('Error submitting the form', error);
    }
  };

  return (
    <div>
      {/* Navigation Bar */}
      <Navbar>
        <NavItem href="#dashboard">Dashboard</NavItem>
        <NavItem href="#predict">Predict</NavItem>
        <NavItem href="#study">Study</NavItem>
        <NavItem href="#about">About</NavItem>
      </Navbar>

      {/* Animated Text and Input Card */}
      <motion.div
        initial={{ opacity: 0.5, y: 100 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{
          delay: 0.3,
          duration: 0.8,
          ease: "easeInOut",
        }}
        className="mt-8 bg-gradient-to-br from-slate-300 to-slate-500 py-2 bg-clip-text text-center text-2xl font-medium tracking-tight text-transparent md:text-4xl"
      >
        Enter Desired Values
        <InputCard onSubmit={handleSubmit}>
          <InputField
            type="text"
            placeholder="Desired Elongation"
            value={elongation}
            onChange={(e) => setElongation(e.target.value)}
          />
          <InputField
            type="text"
            placeholder="Desired UTS"
            value={uts}
            onChange={(e) => setUts(e.target.value)}
          />
          <InputField
            type="text"
            placeholder="Desired Conductivity"
            value={conductivity}
            onChange={(e) => setConductivity(e.target.value)}
          />
          <SubmitButton type="submit">Submit</SubmitButton>
        </InputCard>
      </motion.div>
    </div>
  );
}

export const LampContainer = ({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) => {
  return (
    <div
      className={cn(
        "relative flex min-h-screen flex-col items-center justify-center overflow-hidden bg-slate-950 w-full rounded-md z-0",
        className
      )}
    >
      <div className="relative flex w-full flex-1 scale-y-125 items-center justify-center isolate z-0 ">
        <motion.div
          initial={{ opacity: 0.5, width: "15rem" }}
          whileInView={{ opacity: 1, width: "30rem" }}
          transition={{
            delay: 0.3,
            duration: 0.8,
            ease: "easeInOut",
          }}
          style={{
            backgroundImage: `conic-gradient(var(--conic-position), var(--tw-gradient-stops))`,
          }}
          className="absolute inset-auto right-1/2 h-56 overflow-visible w-[30rem] bg-gradient-conic from-cyan-500 via-transparent to-transparent text-white [--conic-position:from_70deg_at_center_top]"
        >
          <div className="absolute w-[100%] left-0 bg-slate-950 h-40 bottom-0 z-20 [mask-image:linear-gradient(to_top,white,transparent)]" />
          <div className="absolute w-40 h-[100%] left-0 bg-slate-950 bottom-0 z-20 [mask-image:linear-gradient(to_right,white,transparent)]" />
        </motion.div>

        <motion.div
          initial={{ opacity: 0.5, width: "15rem" }}
          whileInView={{ opacity: 1, width: "30rem" }}
          transition={{
            delay: 0.3,
            duration: 0.8,
            ease: "easeInOut",
          }}
          style={{
            backgroundImage: `conic-gradient(var(--conic-position), var(--tw-gradient-stops))`,
          }}
          className="absolute inset-auto left-1/2 h-56 w-[30rem] bg-gradient-conic from-transparent via-transparent to-cyan-500 text-white [--conic-position:from_290deg_at_center_top]"
        >
          <div className="absolute w-40 h-[100%] right-0 bg-slate-950 bottom-0 z-20 [mask-image:linear-gradient(to_left,white,transparent)]" />
          <div className="absolute w-[100%] right-0 bg-slate-950 h-40 bottom-0 z-20 [mask-image:linear-gradient(to_top,white,transparent)]" />
        </motion.div>
        <div className="absolute top-1/2 h-48 w-full translate-y-12 scale-x-150 bg-slate-950 blur-2xl"></div>
        <div className="absolute top-1/2 z-50 h-48 w-full bg-transparent opacity-10 backdrop-blur-md"></div>
        <div className="absolute inset-auto z-50 h-36 w-[28rem] -translate-y-1/2 rounded-full bg-cyan-500 opacity-50 blur-3xl"></div>
        <motion.div
          initial={{ width: "8rem" }}
          whileInView={{ width: "16rem" }}
          transition={{
            delay: 0.3,
            duration: 0.8,
            ease: "easeInOut",
          }}
          className="absolute inset-auto z-30 h-36 w-64 -translate-y-[6rem] rounded-full bg-cyan-400 blur-2xl"
        ></motion.div>
        <motion.div
          initial={{ width: "15rem" }}
          whileInView={{ width: "30rem" }}
          transition={{
            delay: 0.3,
            duration: 0.8,
            ease: "easeInOut",
          }}
          className="absolute inset-auto z-50 h-0.5 w-[30rem] -translate-y-[7rem] bg-cyan-400 "
        ></motion.div>
        <div className="absolute inset-auto z-40 h-44 w-full -translate-y-[12.5rem] bg-slate-950 "></div>
      </div>

      <div className="relative z-50 flex -translate-y-80 flex-col items-center px-5">
        {children}
      </div>
    </div>
  );
};
