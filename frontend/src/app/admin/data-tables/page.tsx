'use client';
import { Box, Text, Image, VStack } from '@chakra-ui/react';
import React from 'react';

export default function DataTables() {
  const images = [
    { src: '/img/EDA/Corr_heatmap.png', text: 'Correlation Heatmap' },
    { src: '/img/EDA/all_features.png', text: 'Feature Sans Analysis' },
    { src: '/img/EDA/Conductivity.png', text: 'Feature Sans Analysis' },
    { src: '/img/EDA/Elongation.png', text: 'Feature Sans Analysis' },
    { src: '/img/EDA/UTS.png', text: 'Feature C Sans Analysis' },
    { src: '/img/EDA/feature_dist.png', text: 'Feature Distribution' },
    { src: '/img/EDA/target_distribution.png', text: 'Target Distribution' },
  ];

  return (
    <Box borderRadius="20px" mt="80px" bg="white" px={{ base: '20px', lg: '40px' }} py="20px">
      {/* Page Header */}
      <Text fontSize="2xl" fontWeight="bold" mb="20px" textAlign="left">
        Exploratory Data Analysis
      </Text>
      <Box w="100%" h="1px" bg="gray.200" mb="20px" />

      {/* Vertical Stack for Images */}
      <VStack spacing={8} align="stretch">
        {images.map((image, index) => (
          <Box
            key={index}
            bg="white"
            borderRadius="15px"
            boxShadow="none"
            overflow="hidden"
            textAlign="center"
            p="20px"
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
            <Text fontSize="md" color="gray.700" fontWeight="medium">
              {image.text}
            </Text>
          </Box>
        ))}
      </VStack>
    </Box>
  );
}