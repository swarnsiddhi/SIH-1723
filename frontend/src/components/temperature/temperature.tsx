// Chakra imports
import { Box, Flex, Text, Icon, useColorModeValue, Checkbox } from '@chakra-ui/react';
// Custom components
import Card from 'components/card/Card';
import Menu from 'components/menu/MainMenu';
import IconBox from 'components/icons/IconBox';
import MiniStatistics from 'components/card/MiniStatistics'; // Import the Default component
// Assets
import { MdCheckBox, MdDragIndicator } from 'react-icons/md';
import { useEffect, useState } from 'react';
import React from 'react';
// Thermometer component
import Thermometer from 'react-thermometer-component'

export default function Conversion(props: { [x: string]: any }) {
	const { ...rest } = props;

	// Chakra Color Mode
	const textColor = useColorModeValue('secondaryGray.900', 'white');
	const boxBg = useColorModeValue('secondaryGray.300', 'navy.700');
	const brandColor = useColorModeValue('brand.500', 'brand.400');

	// State to hold temperature values
	const [temperatures, setTemperatures] = useState({
		rollingMillTemp: 'N/A',
		castingTemp: 'N/A',
		tundishTemp: 'N/A',
		averageTemp: 'N/A',
	});

	// Fetch data from CSV
	useEffect(() => {
		async function fetchData() {
			const response = await fetch('/data/temperature_data.csv'); // Adjust the path if needed
			const text = await response.text();
			const rows = text.split('\n').map(row => row.split(','));
			// Assuming the CSV format: Parameter, Value
			const latest = rows[rows.length - 2];

			const rollingMillTemp = parseFloat(latest[1]) || NaN;
			const castingTemp = parseFloat(latest[2]) || NaN;
			const tundishTemp = parseFloat(latest[3]) || NaN;

			const averageTemp =
				!isNaN(rollingMillTemp) && !isNaN(castingTemp) && !isNaN(tundishTemp)
					? ((rollingMillTemp + castingTemp + tundishTemp) / 3).toFixed(2)
					: 'N/A';

			setTemperatures({
				rollingMillTemp: rollingMillTemp || 'N/A',
				castingTemp: castingTemp || 'N/A',
				tundishTemp: tundishTemp || 'N/A',
				averageTemp,
			});
		}
		fetchData();
	}, []);

	return (
		<Card p='20px' alignItems='center' flexDirection='row' w='100%' {...rest}>
			{/* Left Side: Thermometer */}
			<Box flex="0 0 auto" pr="20px" ml = "30px">
				<Thermometer
					theme="light"
					value={temperatures.averageTemp === 'N/A' ? 0 : parseFloat(temperatures.averageTemp)}
					max="1600"
					steps="5"
					format="°C"
					size="large"
					height="300"
				/>
			</Box>

			{/* Right Side: Cards */}
			<Flex flex="1" flexDirection="column" gap="20px" ml = "20px">
				<MiniStatistics
					name="Rolling Mill Temperature"
					value={`${temperatures.rollingMillTemp} °C`}
					style={{
						fontSize: '40px',
						padding: '20px',
					}}
				/>
				<MiniStatistics
					name="Casting Temperature"
					value={`${temperatures.castingTemp} °C`}
					style={{
						fontSize: '40px',
						padding: '20px',
					}}
				/>
				<MiniStatistics
					name="Tundish Temperature"
					value={`${temperatures.tundishTemp} °C`}
					style={{
						fontSize: '40px',
						padding: '20px',
					}}
				/>
			</Flex>
		</Card>
	);
}
