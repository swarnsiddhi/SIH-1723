// Chakra imports
import { Box, Button, Flex, Icon, Text, useColorModeValue } from '@chakra-ui/react';
// Custom components
import Card from 'components/card/Card';
import LineChart from 'components/charts/LineChart';
import Papa from 'papaparse';
import { useEffect, useState } from 'react';
import { MdOutlineCalendarToday } from 'react-icons/md';
import { IoCheckmarkCircle } from 'react-icons/io5';
import { getLineChartOptions } from 'variables/charts';

export default function TotalSpent(props: { parameter: string }) {
	const { parameter, ...rest } = props;

	// Chakra Color Mode
	const textColor = useColorModeValue('secondaryGray.900', 'white');
	const textColorSecondary = useColorModeValue('secondaryGray.600', 'white');
	const boxBg = useColorModeValue('secondaryGray.300', 'whiteAlpha.100');
	const iconColor = useColorModeValue('brand.500', 'white');

	// States for fetched values
	const [chartData, setChartData] = useState<any[]>([]);

	// Fetch CSV data
	useEffect(() => {
		const fetchCsv = async () => {
			const response = await fetch('/data/wire rod properties.csv');
			const csvText = await response.text();

			// Parse CSV data
			Papa.parse(csvText, {
				header: true,
				skipEmptyLines: true,
				complete: (results) => {
					const data = results.data;
					setChartData(data);
				},
			});
		};

		fetchCsv();
	}, []);

	// Define color for each parameter
	const parameterColors = {
		UTS: '#1e3a8a',        // Dark Blue for UTS
		Elongation: '#38bdf8',  // Sky Blue for Elongation
		Conductivity: '#fb923c' // Orange for Conductivity
	};

	// Slice chart data to keep only the last 15 entries
	const filteredChartData = chartData
		.slice(-15) // Take the last 15 entries
		.map((d) => ({
			x: d.Coil_No,
			y: parseFloat(d[parameter]),
		}));

	// Line chart data based on selected parameter
	const lineChartData = [
		{
			name: parameter,
			data: filteredChartData,
			color: parameterColors[parameter] || '#000',  // Default to black if no color is found
		},
	];

	// Slice the last 15 dates for the X-axis
	const xAxisData = filteredChartData.map((d) => d.x);

	// Get chart options based on the last 15 dates
	const chartOptions = getLineChartOptions(xAxisData);

	// Extract the last 5 values for the selected parameter
	const parameterValues = chartData
		.slice(-5) // Take the last 5 entries
		.map((d) => ({
			date: d.Coil_No,
			value: parseFloat(d[parameter]),
		}));

	return (
		<Card justifyContent="center" alignItems="center" flexDirection="column" w="100%" mb="0px" {...rest}>
			<Flex justify="space-between" ps="0px" pe="20px" pt="5px" w="100%">
				<Flex align="center" w="100%">
					<Button bg={boxBg} fontSize="sm" fontWeight="500" color={textColorSecondary} borderRadius="7px">
						<Icon as={MdOutlineCalendarToday} color={textColorSecondary} me="4px" />
						{parameter}
					</Button>
				</Flex>
			</Flex>
			<Flex w="100%" flexDirection={{ base: 'column', lg: 'row' }}>
				<Flex flexDirection="column" me="20px" mt="16px">
					<Text color={textColor} fontSize="34px" textAlign="start" fontWeight="700" lineHeight="100%">
					    {parameterValues[parameterValues.length - 1]?.value || 'N/A'}
					</Text>
					<Flex align="center" mb="20px" mt="6px">
						<Icon as={IoCheckmarkCircle} color="green.500" me="8px" />
						<Text color="secondaryGray.600" fontSize="sm" fontWeight="500">
							Live
						</Text>
					</Flex>
					<Box>
						{parameterValues.map((data) => (
							<Text key={data.date} color={textColorSecondary} fontSize="sm" fontWeight="500">
								{data.date}: {data.value || 'N/A'}
							</Text>
						))}
					</Box>
				</Flex>
				<Box minH="260px" minW="75%" mt="auto">
					<LineChart chartData={lineChartData} chartOptions={chartOptions} />
				</Box>
			</Flex>
		</Card>
	);
}
