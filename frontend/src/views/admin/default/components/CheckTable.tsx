import { Flex, Box, Table, Checkbox, Tbody, Td, Text, Th, Thead, Tr, useColorModeValue } from '@chakra-ui/react';
import * as React from 'react';

import {
	createColumnHelper,
	flexRender,
	getCoreRowModel,
	getSortedRowModel,
	SortingState,
	useReactTable
} from '@tanstack/react-table';

// Custom components
import Card from 'components/card/Card';
import Menu from 'components/menu/MainMenu';
import SwitchField from 'components/fields/SwitchField';

type RowObj = {
	parameter: [string];
	original: number;
	difference: number;
	lock: string;
};

const columnHelper = createColumnHelper<RowObj>();

export default function CheckTable(props: { tableData: any }) {
	const { tableData } = props;
	const [sorting, setSorting] = React.useState<SortingState>([]);
	const textColor = useColorModeValue('secondaryGray.900', 'white');
	const borderColor = useColorModeValue('gray.200', 'whiteAlpha.100');
	let defaultData = tableData;

	const columns = [
		columnHelper.accessor('parameter', {
			id: 'parameter',
			header: () => (
				<Text fontSize={{ sm: '10px', lg: '12px' }} color='gray.400'>
					PARAMETER
				</Text>
			),
			cell: (info: any) => (
				<Flex align='center'>
					<Text color={textColor} fontSize='sm' fontWeight='700'>
						{info.getValue()[0]}
					</Text>
				</Flex>
			)
		}),
		columnHelper.accessor('original', {
			id: 'original',
			header: () => (
				<Text fontSize={{ sm: '10px', lg: '12px' }} color='gray.400'>
					ORIGINAL
				</Text>
			),
			cell: (info) => (
				<Text color={textColor} fontSize='sm' fontWeight='700'>
					{info.getValue()}
				</Text>
			)
		}),
		columnHelper.accessor('difference', {
			id: 'difference',
			header: () => (
				<Text fontSize={{ sm: '10px', lg: '12px' }} color='gray.400'>
					DIFFERENCE
				</Text>
			),
			cell: (info) => {
				const value = info.getValue();
				const color = value >= 0 ? 'green.400' : 'red.400';
				return (
					<Text color={color} fontSize='sm' fontWeight='700'>
						{value}
					</Text>
				);
			}
		}),
		columnHelper.accessor('lock', {
			id: 'lock',
			header: () => (
				<Text fontSize={{ sm: '10px', lg: '12px' }} color='gray.400'>
					LOCK
				</Text>
			),
			cell: () => <SwitchField reversed={true} fontSize='sm' mb='20px' id='2' />
		})
	];

	const [data, setData] = React.useState(() => [...defaultData]);
	const table = useReactTable({
		data,
		columns,
		state: {
			sorting
		},
		onSortingChange: setSorting,
		getCoreRowModel: getCoreRowModel(),
		getSortedRowModel: getSortedRowModel(),
		debugTable: true
	});

	return (
		<Card flexDirection='column' w='100%' px='0px' overflowX={{ sm: 'scroll', lg: 'hidden' }}>
			<Flex px='25px' mb="8px" justifyContent='space-between' align='center'>
				<Text color={textColor} fontSize='22px' mb="4px" fontWeight='700' lineHeight='100%'>
					Check Table
				</Text>
				<Menu />
			</Flex>
			<Box maxH="460px" overflowY="scroll">
				<Table variant='simple' color='gray.500' mb='24px' mt="12px">
					<Thead>
						{table.getHeaderGroups().map((headerGroup) => (
							<Tr  key={headerGroup.id}>
								{headerGroup.headers.map((header) => {
									return (
										<Th
											key={header.id}
											colSpan={header.colSpan}
											pe='10px'
											borderColor={borderColor}
											cursor='pointer'
											onClick={header.column.getToggleSortingHandler()}>
											<Flex
												justifyContent='space-between'
												align='center'
												fontSize={{ sm: '10px', lg: '12px' }}
												color='gray.400'>
												{flexRender(header.column.columnDef.header, header.getContext())}{{
													asc: '',
													desc: '',
												}[header.column.getIsSorted() as string] ?? null}
											</Flex>
										</Th>
									);
								})}
							</Tr>
						))}
					</Thead>
					<Tbody>
						{table.getRowModel().rows.slice(0, 25).map((row) => {
							return (
								<Tr key={row.id}>
									{row.getVisibleCells().map((cell) => {
										return (
											<Td
												key={cell.id}
												fontSize={{ sm: '14px' }}
												minW={{ sm: '150px', md: '200px', lg: 'auto' }}
												borderColor='transparent'>
												{flexRender(cell.column.columnDef.cell, cell.getContext())}
											</Td>
										);
									})}
								</Tr>
							);
						})}
					</Tbody>
				</Table>
			</Box>
		</Card>
	);
}
