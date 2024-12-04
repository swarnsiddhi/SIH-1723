"use client";

import {
  Box,
  Flex,
  Table,
  Tbody,
  Td,
  Th,
  Thead,
  Tr,
  SimpleGrid,
  useColorModeValue,
  Spinner,
  Text,
} from "@chakra-ui/react";
import { useEffect, useState } from "react";
import MiniStatistics from "components/card/MiniStatistics";
import IconBox from "components/icons/IconBox";
import { MdAttachMoney, MdBarChart } from "react-icons/md";

export default function Dashboard() {
  // Chakra Color Mode
  const brandColor = useColorModeValue("brand.500", "white");
  const boxBg = useColorModeValue("secondaryGray.300", "whiteAlpha.100");

  // States for fetched values
  const [utsValue, setUtsValue] = useState(null);
  const [elongationValue, setElongationValue] = useState(null);
  const [conductivityValue, setConductivityValue] = useState(null);
  const [differences, setDifferences] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch data from the API
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);

        const apiUrl = process.env.REACT_APP_API_URL || "http://localhost:5000";
        console.log("Fetching data from:", `${apiUrl}/api/final_prediction`);

        const response = await fetch(`${apiUrl}/api/final_prediction`);
        if (!response.ok) {
          throw new Error(`HTTP Error: ${response.status}`);
        }

        const data = await response.json();
        console.log("Data fetched successfully:", data);

        setUtsValue(data.predictions.uts || 0);
        setElongationValue(data.predictions.elongation || 0);
        setConductivityValue(data.predictions.conductivity || 0);
        setDifferences(data.differences || {});
      } catch (error) {
        console.error("Error fetching data:", error.message);
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <Flex justify="center" align="center" h="100vh">
        <Spinner size="xl" />
        <Text ml="4">Loading data...</Text>
      </Flex>
    );
  }

  if (error) {
    return (
      <Flex justify="center" align="center" h="100vh">
        <Text color="red.500" fontSize="lg">
          Error: {error}
        </Text>
      </Flex>
    );
  }

  return (
    <Box pt={{ base: "130px", md: "80px", xl: "80px" }}>
      {/* Cards for Predictions */}
      <SimpleGrid columns={{ base: 1, md: 2, xl: 3 }} gap="20px" mb="20px">
        <MiniStatistics
          startContent={
            <IconBox
              w="56px"
              h="56px"
              bg={boxBg}
              icon={<MdBarChart size="32px" color={brandColor} />}
            />
          }
          name="UTS"
          value={`${utsValue}`}
        />
        <MiniStatistics
          startContent={
            <IconBox
              w="56px"
              h="56px"
              bg={boxBg}
              icon={<MdAttachMoney size="32px" color={brandColor} />}
            />
          }
          name="Elongation"
          value={`${elongationValue}`}
        />
        <MiniStatistics
          name="Conductivity"
          value={`${conductivityValue}`}
        />
      </SimpleGrid>

      {/* Table for Differences */}
      <Box mt="20px" p="4" bg={boxBg} rounded="md">
        <Table variant="simple">
          <Thead>
            <Tr>
              <Th>Parameter</Th>
              <Th>Difference</Th>
            </Tr>
          </Thead>
          <Tbody>
            {Object.entries(differences).map(([key, value]) => (
              <Tr key={key}>
                <Td>{key}</Td>
                <Td>{value}</Td>
              </Tr>
            ))}
          </Tbody>
        </Table>
      </Box>
    </Box>
  );
}
