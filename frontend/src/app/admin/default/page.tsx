'use client';
/*!
  _   _  ___  ____  ___ ________  _   _   _   _ ___   
 | | | |/ _ \|  _ \|_ _|__  / _ \| \ | | | | | |_ _| 
 | |_| | | | | |_) || |  / / | | |  \| | | | | || | 
 |  _  | |_| |  _ < | | / /| |_| | |\  | | |_| || |
 |_| |_|\___/|_| \_\___/____\___/|_| \_|  \___/|___|
                                                                                                                                                                                                                                                                                                                                       
=========================================================
* Horizon UI - v1.1.0
=========================================================

* Product Page: https://www.horizon-ui.com/
* Copyright 2022 Horizon UI (https://www.horizon-ui.com/)

* Designed and Coded by Simmmple

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/

import {
  Box,
  Flex,
  FormLabel,
  Image,
  Icon,
  Select,
  SimpleGrid,
  useColorModeValue,
  Spinner,
  Text,
} from '@chakra-ui/react';
// Custom components
// import MiniCalendar from 'components/calendar/MiniCalendar';
import MiniStatistics from 'components/card/MiniStatistics';
import IconBox from 'components/icons/IconBox';
import {
  MdAddTask,
  MdAttachMoney,
  MdBarChart,
  MdFileCopy,
} from 'react-icons/md';
import CheckTable from 'views/admin/default/components/CheckTable';
import ComplexTable from 'views/admin/default/components/ComplexTable';
import DailyTraffic from 'views/admin/default/components/DailyTraffic';
import PieCard from 'views/admin/default/components/PieCard';
import Tasks from 'views/admin/default/components/Tasks';
import TotalSpent from 'views/admin/default/components/TotalSpent';
import WeeklyRevenue from 'views/admin/default/components/WeeklyRevenue';
import tableDataCheck from 'views/admin/default/variables/tableDataCheck';
import tableDataComplex from 'views/admin/default/variables/tableDataComplex';
import { useEffect, useState } from "react";
// Assets
import Usa from 'img/dashboards/usa.png';

export default function Default() {
  // Chakra Color Mode

  const brandColor = useColorModeValue('brand.500', 'white');
  const boxBg = useColorModeValue('secondaryGray.300', 'whiteAlpha.100');

  const [utsValue, setUtsValue] = useState(null);
  const [elongationValue, setElongationValue] = useState(null);
  const [conductivityValue, setConductivityValue] = useState(null);
  const [tableDataCheck, setTableDataCheck] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch data from the API
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);

        const apiUrl = process.env.REACT_APP_API_URL || "http://localhost:5000";
        const response = await fetch(`${apiUrl}/api/final_prediction`);
        if (!response.ok) {
          throw new Error(`HTTP Error: ${response.status}`);
        }

        const data = await response.json();

        // Update values for the stats
        setUtsValue(data.predictions.uts || 0);
        setElongationValue(data.predictions.elongation || 0);
        setConductivityValue(data.predictions.conductivity || 0);

        // Transform data for the table
        const updatedTableData = Object.keys(data.differences).map((key) => ({
          parameter: [key],
          original: data.original[key],
          difference: data.differences[key],
          lock: false,
        }));

        setTableDataCheck(updatedTableData);
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

  return (
    <Box pt={{ base: '130px', md: '80px', xl: '80px' }}>
      <SimpleGrid
        columns={{ base: 1, md: 2, lg: 3, '2xl': 3 }}
        gap="20px"
        mb="20px"
      >
        <MiniStatistics
          startContent={
            <IconBox
              w="70px"
              h="56px"
              bg={boxBg}
              icon={
                <Icon w="64px" h="32px" as={MdBarChart} color={brandColor} />
              }
            />
          }
          name="Ultimate Tensile Strength"
          value={`${utsValue}`}
        />
        <MiniStatistics
          startContent={
            <IconBox
              w="70px"
              h="56px"
              bg={boxBg}
              icon={
                <Icon w="64px" h="32px" as={MdAttachMoney} color={brandColor} />
              }
            />
          }
          name="Elongation"
          value={`${elongationValue}`}
        />
        <MiniStatistics
          startContent={
            <IconBox
              w="70px"
              h="56px"
              bg={boxBg}
              icon={
                <Icon w="64px" h="32px" as={MdFileCopy} color={brandColor} />
              }
            />
          }
          name="Conductivity"
          value={`${conductivityValue}`}
        />
      </SimpleGrid>
      <SimpleGrid columns={{ base: 1, md: 1, xl: 2 }} gap="20px" mb="20px">
        <CheckTable tableData={tableDataCheck} />
        <SimpleGrid columns={{ base: 1, md: 2, xl: 2 }} gap="20px">
          <DailyTraffic />
          <PieCard />
        </SimpleGrid>
      </SimpleGrid>

      <SimpleGrid columns={{ base: 1, md: 2, xl: 2 }} gap="20px" mb="20px">
        <TotalSpent />
        <WeeklyRevenue />
      </SimpleGrid>
      <SimpleGrid columns={{ base: 1, md: 1, xl: 2 }} gap="20px" mb="20px">
        <ComplexTable tableData={tableDataComplex} />
        <SimpleGrid columns={{ base: 1, md: 2, xl: 2 }} gap="20px">
          <Tasks />
          {/* <MiniCalendar h="100%" minW="100%" selectRange={false} /> */}
        </SimpleGrid>
      </SimpleGrid>
    </Box>
  );
}