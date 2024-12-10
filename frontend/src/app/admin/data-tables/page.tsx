'use client';
import { Box, VStack, Text, Image } from '@chakra-ui/react';
import React from 'react';

export default function DataTables() {
  const images = [
    {
      src: '/img/EDA/Corr_heatmap.png',
      text: 'Correlation Heatmap',
    },
    {
      src: '/img/EDA/Featue_sans.png',
      text: 'Feature Sans Analysis',
    },
    {
      src: '/img/EDA/Feature_C_sans.png',
      text: 'Feature C Sans Analysis',
    },
    {
      src: '/img/EDA/feature_dist.png',
      text: 'Feature Distribution',
    },
    {
      src: '/img/EDA/Feature_E_sans.png',
      text: 'Feature E Sans Analysis',
    },
    {
      src: '/img/EDA/Feature_U_sans.png',
      text: 'Feature U Sans Analysis',
    },
    {
      src: '/img/EDA/target_distribution.png',
      text: 'Target Distribution',
    },
  ];                    

  return (
    <Box borderRadius='20px' mt='80px' bg="white">
      {/* Page Header */}
      <Text fontSize="2xl" fontWeight="bold" pt='20px' mb="20px" textAlign="left" ml='40px '>
        Exploratory Data Analysis
      </Text>
      <Box
        w="100%"
        h="1px"
        bg="gray.200"
        my="10px"
      />
      {/* Vertical Stack for Cards */}
      <VStack spacing="20px" px={{ base: '20px', lg: '40px' }}>
        {images.map((image, index) => (
          <Box
            key={index}
            bg="white"
            borderRadius="15px"
            boxShadow="none"
            overflow="hidden"
            p="20px"
            w="100%" // Make card take full width of container
            maxW="800px" // Limit card width
          >
            {/* Image */}
            <Image
              src={image.src}
              alt={`Image ${index + 1}`}
              objectFit="cover"
              w="100%"
              borderRadius="12px"
              mb="15px"
            />
            {/* Description */}
            <Text fontSize="sm" color="gray.500" textAlign="center">
              {image.text}
            </Text>
          </Box>
        ))}
      </VStack>
    </Box>
  );
}
