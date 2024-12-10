'use client';
import { Box, Text, Image, VStack } from '@chakra-ui/react';
import React from 'react';
import AdminLayout from 'layouts/admin';

export default function EDAComponent() {
  return (
    <Box
      pt={{ base: '130px', md: '80px', xl: '80px' }}
      bg="white"
      borderRadius="15px"
      boxShadow="lg"
      p="20px"
    >
      {/* Headline */}
      <Text fontSize="2xl" fontWeight="bold" mb="20px" textAlign="center">
        EDA
      </Text>

      <VStack spacing="40px">
        {/* First Image Section */}
        <Box w="100%" borderRadius="15px" overflow="hidden">
          <Image
            src="/path/to/your-first-image.jpg" // Replace with the actual image path
            alt="First EDA Image"
            objectFit="cover"
            w="100%"
          />
        </Box>
        <Text fontSize="sm" color="gray.500" textAlign="center">
          This is the description text for the first image.
        </Text>

        {/* Second Image Section */}
        <Box w="100%" borderRadius="15px" overflow="hidden">
          <Image
            src="/path/to/your-second-image.jpg" // Replace with the actual image path
            alt="Second EDA Image"
            objectFit="cover"
            w="100%"
          />
        </Box>
        <Text fontSize="sm" color="gray.500" textAlign="center">
          This is the description text for the second image.
        </Text>
      </VStack>
    </Box>
  );
}
