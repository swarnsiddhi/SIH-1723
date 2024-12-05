'use client';

import {
  Box,
  SimpleGrid,
  useColorModeValue,
  Input,
  FormControl,
  FormLabel,
  InputGroup,
  InputRightAddon,
  Icon,
} from '@chakra-ui/react';
import { MdBarChart, MdAttachMoney, MdFileCopy } from 'react-icons/md';
import { useState } from 'react';

export default function Default() {
  const brandColor = useColorModeValue('brand.500', 'white');
  const boxBg = useColorModeValue('secondaryGray.300', 'whiteAlpha.100');
  const hoverBg = useColorModeValue('gray.200', 'gray.700');
  const hoverColor = useColorModeValue('black', 'white');

  // State for input values
  const [values, setValues] = useState({
    ultimateTensileStrength: '',
    elongation: '',
    conductivity: '',
  });

  // Handler for input changes
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setValues({ ...values, [name]: value });
  };

  return (
    <Box pt={{ base: '130px', md: '80px', xl: '80px' }}>
      <SimpleGrid
        columns={{ base: 1, md: 2, lg: 3, '2xl': 3 }}
        gap="20px"
        mb="20px"
      >
        {/* Ultimate Tensile Strength */}
        <FormControl>
          <FormLabel
            display="flex"
            alignItems="center"
            gap="8px"
            _hover={{ color: brandColor, cursor: 'pointer' }}
          >
            <Box
              w="50px"
              h="50px"
              bg={boxBg}
              borderRadius="md"
              display="flex"
              alignItems="center"
              justifyContent="center"
              transition="transform 0.2s ease"
              _hover={{ transform: 'scale(1.1)', cursor: 'pointer' }}
            >
              <Icon as={MdBarChart} boxSize={6} color={brandColor} />
            </Box>
            Ultimate Tensile Strength
          </FormLabel>
          <InputGroup>
            <Input
              name="ultimateTensileStrength"
              value={values.ultimateTensileStrength}
              onChange={handleInputChange}
              type="number"
              placeholder="Enter Ultimate Tensile Strength"
            />
            <InputRightAddon
              bg={boxBg}
              _hover={{
                bg: hoverBg,
                color: hoverColor,
                cursor: 'pointer',
              }}
            >
              MPa
            </InputRightAddon>
          </InputGroup>
        </FormControl>

        {/* Elongation */}
        <FormControl>
          <FormLabel
            display="flex"
            alignItems="center"
            gap="8px"
            _hover={{ color: brandColor, cursor: 'pointer' }}
          >
            <Box
              w="50px"
              h="50px"
              bg={boxBg}
              borderRadius="md"
              display="flex"
              alignItems="center"
              justifyContent="center"
              transition="transform 0.2s ease"
              _hover={{ transform: 'scale(1.1)', cursor: 'pointer' }}
            >
              <Icon as={MdAttachMoney} boxSize={6} color={brandColor} />
            </Box>
            Elongation
          </FormLabel>
          <InputGroup>
            <Input
              name="elongation"
              value={values.elongation}
              onChange={handleInputChange}
              type="number"
              placeholder="Enter Elongation"
            />
            <InputRightAddon
              bg={boxBg}
              _hover={{
                bg: hoverBg,
                color: hoverColor,
                cursor: 'pointer',
              }}
            >
              %
            </InputRightAddon>
          </InputGroup>
        </FormControl>

        {/* Conductivity */}
        <FormControl>
          <FormLabel
            display="flex"
            alignItems="center"
            gap="8px"
            _hover={{ color: brandColor, cursor: 'pointer' }}
          >
            <Box
              w="50px"
              h="50px"
              bg={boxBg}
              borderRadius="md"
              display="flex"
              alignItems="center"
              justifyContent="center"
              transition="transform 0.2s ease"
              _hover={{ transform: 'scale(1.1)', cursor: 'pointer' }}
            >
              <Icon as={MdFileCopy} boxSize={6} color={brandColor} />
            </Box>
            Conductivity
          </FormLabel>
          <InputGroup>
            <Input
              name="conductivity"
              value={values.conductivity}
              onChange={handleInputChange}
              type="number"
              placeholder="Enter Conductivity"
            />
            <InputRightAddon
              bg={boxBg}
              _hover={{
                bg: hoverBg,
                color: hoverColor,
                cursor: 'pointer',
              }}
            >
              S/m
            </InputRightAddon>
          </InputGroup>
        </FormControl>
      </SimpleGrid>
    </Box>
  );
}
