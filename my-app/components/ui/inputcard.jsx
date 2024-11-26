
"use client";
import React from "react";
import { cn } from "@/lib/utils";
import Image from "next/image";

const ModernInputCard = () => {
    return (
      <div className="flex justify-center items-center h-screen bg-gradient-to-b from-gray-200 to-white">
        <div className="w-full max-w-md p-6 bg-white shadow-lg rounded-lg border border-gray-300">
          <h2 className="gradient-to-br from-slate-300 to-slate-500 py-4 bg-clip-text text-center text-4xl font-medium tracking-tight text-transparent md:text-7xl">
            Input Desired Parameters
          </h2>
          <form className="space-y-4 mt-6">
            <div>
              <label
                htmlFor="elongation"
                className="block text-sm font-medium text-gray-700"
              >
                Enter Desired Elongation
              </label>
              <input
                type="number"
                id="elongation"
                className="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                placeholder="e.g., 5%"
              />
            </div>
            <div>
              <label
                htmlFor="uts"
                className="block text-sm font-medium text-gray-700"
              >
                Enter Desired UTS
              </label>
              <input
                type="number"
                id="uts"
                className="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                placeholder="e.g., 500 MPa"
              />
            </div>
            <div>
              <label
                htmlFor="conductivity"
                className="block text-sm font-medium text-gray-700"
              >
                Enter Desired Conductivity
              </label>
              <input
                type="number"
                id="conductivity"
                className="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                placeholder="e.g., 80%"
              />
            </div>
            <button
              type="submit"
              className="w-full py-2 px-4 bg-indigo-500 text-white font-medium text-sm leading-5 rounded-lg shadow-md hover:bg-indigo-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Submit
            </button>
          </form>
        </div>
      </div>
    );
  };

  export function CardDemo() {
    return (
      <div className="max-w-xs w-full group/card">
        <div
          className={cn(
            " cursor-pointer overflow-hidden relative card h-96 rounded-md shadow-xl  max-w-sm mx-auto backgroundImage flex flex-col justify-between p-4",
            "bg-[url(https://images.unsplash.com/photo-1544077960-604201fe74bc?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1651&q=80)] bg-cover"
          )}
        >
          <div className="absolute w-full h-full top-0 left-0 transition duration-300 group-hover/card:bg-black opacity-60"></div>
          <div className="flex flex-row items-center space-x-4 z-10">
            <Image
              height="100"
              width="100"
              alt="Avatar"
              src="/manu.png"
              className="h-10 w-10 rounded-full border-2 object-cover"
            />
            <div className="flex flex-col">
              <p className="font-normal text-base text-gray-50 relative z-10">
                Manu Arora
              </p>
              <p className="text-sm text-gray-400">2 min read</p>
            </div>
          </div>
          <div className="text content">
            <h1 className="font-bold text-xl md:text-2xl text-gray-50 relative z-10">
              Author Card
            </h1>
            <p className="font-normal text-sm text-gray-50 relative z-10 my-4">
              Card with Author avatar, complete name and time to read - most
              suitable for blogs.
            </p>
          </div>
        </div>
      </div>
    );
  }
  
  export default ModernInputCard;
  